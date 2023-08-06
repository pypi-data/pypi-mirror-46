# -*- coding: utf-8 -*-
"""JWE (JSON Web Encryption) module for the JOSE package."""

# Created: 2018-07-30 Guy K. Kloss <guy@mysinglesource.io>
#
# (c) 2018-2019 by SingleSource Limited, Auckland, New Zealand
#     http://mysinglesource.io/
#     Apache 2.0 Licence.
#
# This work is licensed under the Apache 2.0 open source licence.
# Terms and conditions apply.
#
# You should have received a copy of the licence along with this
# program.

__author__ = 'Guy K. Kloss <guy@mysinglesource.io>'

import base64
from collections import OrderedDict
import nacl.utils
from typing import Optional, Union, Callable

from sspyjose import Jose
from sspyjose import cryptography_aead_wrap as cryptography_aead
from sspyjose import nacl_aead_wrap as nacl_aead
from sspyjose import utils
from sspyjose.jwk import (Jwk,
                          X25519Jwk)


def _int_to_bytes(value: int) -> bytes:
    """
    Convert an unsigned integer to a 32 bit byte representation.

    The result is in big-endian format.

    :param value: The (unsigned) integer value to convert.
    :return: Byte representation.
    """
    return value.to_bytes(4, byteorder='big', signed=False)


class Jwe(Jose):
    """
    JSON Web Encryption (JWE) RFC 7516.

    Only implements the following cipher suites:

    - C20P - symmetric, 256-bit key size, 96-bit nonce
      [https://tools.ietf.org/id/draft-amringer-jose-chacha-00.txt]
      (RFC 7539 and RFC 8439).
    - A256GCM - symmetric, 256-bit key size, 96-bit nonce, no key wrapping
      (basic RFC 7516).
    - X25519 - public key-based, 256-bit key size (RFC 8037).
    - `unsecured` - non-standard, unencrypted, 'symmetric' JWE
      (contains an `{"alg": "unsecured"}` header).
    """

    _header = None  # type: Optional[dict]
    """Protected header."""
    _key = None  # type: Optional[bytes]
    """Encrypted key."""
    _nonce = None  # type: Optional[bytes]
    """Nonce/initialisation vector."""
    _message = None  # type: Optional[dict]
    """Plain text message."""
    _ciphertext = None  # type: Optional[bytes]
    """Ciphertext."""
    _tag = None  # type: Optional[bytes]
    """Authentication tag/MAC."""
    _SERIALISATION_PARTS = ('header', 'key', 'nonce', 'ciphertext', 'tag')
    """Parts of the JWE serialisation specification."""
    _jwk = None  # type: Optional[Jwk]
    """JWK to use for en/decryption."""
    _message_bytes = None  # type: Optional[bytes]
    """Retains the byte serialisation of the message content in verbatim."""

    def __init__(self, *,
                 from_compact: Union[bytes, str, None] = None,
                 jwk: Optional[Jwk] = None):
        """
        Constructor.

        :param from_compact: If present, load data from compact ASCII JWE
            serialisation format.
        :param jwk: JWK to use for en-/decryption.
        """
        super().__init__()
        if from_compact:
            self.load_compact(from_compact)
        if jwk:
            self._jwk = jwk

    @classmethod
    def get_instance(
            cls, *,
            enc: Optional[str] = None,
            alg: Optional[str] = None,
            from_compact: Union[bytes, str, None] = None,
            jwk: Optional[Jwk] = None) -> 'Jwe':
        """
        Get an instance of a specific JWE object by algorithm via factory.

        :param enc: Specific encryption indicator
            (default: {Jose.DEFAULT_ENC}).
        :param alg: Specific algorithm indicator (default: 'dir').
        :param from_compact: Load data from compact ASCII JWE serialisation
            format (default: None).
        :param jwk: JWK to use for en-/decryption (default: None).
        :return: A {Jwe} object.
        """
        if enc is None:
            # Try some places to determine the required value for `enc`.
            # First from given key.
            if jwk:
                enc = jwk._data.get('alg')
            # Still nothing, try from JWE content.
            if enc is None and from_compact:
                if isinstance(from_compact, bytes):
                    from_compact = from_compact.decode('utf-8')
                elements = from_compact.split('.')
                content = utils.base64_to_dict(elements[0])
                enc = content.get('enc')
                alg = content.get('alg')
            # Nothing, so go with the default.
            if enc is None and alg != 'unsecured':
                enc = Jose.DEFAULT_ENC
        alg = alg or 'dir'
        klass = _CLASS_MAPPING.get((enc, alg))
        if klass:
            return klass(from_compact=from_compact, jwk=jwk)
        raise RuntimeError(
            'No suitable JWE type implemented for enc={} and alg={}.'
            .format(enc, alg))

    @property
    def header(self) -> dict:
        """Protected header."""
        return self._header

    @property
    def key(self) -> bytes:
        """Encrypted key."""
        return self._key

    @property
    def nonce(self) -> bytes:
        """Nonce/initialisation vector."""
        return self._nonce

    @property
    def message(self) -> dict:
        """Plain text message."""
        return self._message

    @message.setter
    def message(self, value: dict):
        """
        Set plain text message. This clears any ciphertext attribute value.

        :param value: Content in bytes.
        """
        self._message = value
        self._message_bytes = None
        self._ciphertext = None
        self._tag = None

    @property
    def ciphertext(self) -> bytes:
        """Ciphertext."""
        return self._ciphertext

    @ciphertext.setter
    def ciphertext(self, value: bytes):
        """
        Set ciphertext. This clears any message attribute value.

        :param value: Content in bytes.
        """
        self._ciphertext = value
        self._message = None

    @property
    def tag(self) -> bytes:  # noqa: D401
        """Authentication tag/MAC."""
        return self._tag

    @tag.setter
    def tag(self, value: bytes):
        """
        Set authentication tag/MAC.

        :param value: Content in bytes.
        """
        self._tag = value

    @property
    def jwk(self) -> Jwk:
        """En/decryption key for this JWE."""
        return self._jwk

    @jwk.setter
    def jwk(self, value: Jwk):
        """
        Set en/decryption key for this JWE.

        :param value: JWK key object.
        """
        self._jwk = value

    def to_dict(self) -> dict:
        """
        Express the JWE as a JOSE compliant dictionary.
        """
        result = OrderedDict()
        for item in self._SERIALISATION_PARTS:
            result[item] = getattr(self, '_' + item)
        # JSONify the header.
        result['header'] = utils.dict_to_base64(result['header'])
        return result

    def to_json(self) -> str:
        """
        Serialise the JWE to JOSE compliant JSON.
        """
        return utils.dict_to_json(self.to_dict())

    def serialise(self) -> str:
        """
        Serialise the JWE to JOSE (compact) form.
        """
        parts = [getattr(self, '_' + item)
                 for item in self._SERIALISATION_PARTS]
        # JSONify the header.
        parts[0] = utils.dict_to_json(parts[0]).encode('utf-8')
        parts = [utils.bytes_to_string(item)
                 if item else '' for item in parts]
        return '.'.join(parts)

    @property
    def json(self) -> str:  # noqa: D401
        """Serialised JWE as JOSE compliant JSON."""
        return self.to_json()

    def load_compact(self, data: Union[bytes, str]):
        """
        Load JWE compact serialisation format.

        :param data: Serialisation data.
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        parts = data.split(b'.')
        if len(parts) != len(self._SERIALISATION_PARTS):
            raise ValueError(
                'Trying to load JWE compact serialisation with other than'
                ' {} parts: {} found.'
                .format(len(self._SERIALISATION_PARTS), len(parts)))
        parts = [base64.urlsafe_b64decode(item + b'==')
                 if item != b'' else None
                 for item in parts]
        content = dict(zip(self._SERIALISATION_PARTS, parts))
        content['header'] = utils.json_to_dict(content['header'])
        for key, value in content.items():
            setattr(self, '_' + key, value)

    def get_message_bytes(self) -> bytes:
        """
        Get canonical message representation as bytes.
        """
        if self._message_bytes is None:
            self._message_bytes = utils.dict_to_json(
                self._message).encode('utf-8')
        return self._message_bytes

    def encrypt(self) -> (bytes, bytes):
        """
        Encrypt the JWE message, and store the resulting ciphertext and tag.

        :return: Tuple (ciphertext, tag).
        """
        raise NotImplementedError('Needs to be implemented by child class.')

    def decrypt(self) -> bytes:
        """
        Decrypts the JWE ciphertext and stores the resulting message.

        :return: Decrypted message.
        """
        raise NotImplementedError('Needs to be implemented by child class.')


class SymmetricJwe(Jwe):
    """
    Symmetric key encryption.
    """

    _DEFAULT_HEADER = None  # type: Optional[dict]
    _KEYBYTES = 0  # type: Optional[int]
    _NONCEBYTES = 0  # type: Optional[int]
    _aead_encrypt_function = None  # type: Optional[Callable]
    _aead_decrypt_function = None  # type: Optional[Callable]

    def encrypt(self) -> (bytes, bytes):
        """
        Encrypt the JWE message, and store the resulting ciphertext and tag.

        :return: Tuple (ciphertext, tag).
        """
        plaintext = self.get_message_bytes()
        self._header = self._DEFAULT_HEADER.copy()
        header_bytes = utils.dict_to_base64(self._header).encode('utf-8')
        if self._header['alg'] != 'unsecured':
            self._nonce = nacl.utils.random(nacl_aead.NONCEBYTES)
        else:
            result = plaintext, None
        if self.__class__._aead_encrypt_function:
            result = self.__class__._aead_encrypt_function(
                plaintext, header_bytes, self._nonce, self._jwk.k)
        self._ciphertext, self._tag = result
        return result

    def decrypt(self, *, allow_unsecured: bool = False) -> bytes:
        """
        Decrypts the JWE ciphertext and stores the resulting message.

        :param allow_unsecured: Allows explicitly for access to non-standard,
            "unsecured" JWEs (default: forbidden).
        :return: Decrypted message.
        """
        header_bytes = utils.dict_to_base64(self._header).encode('utf-8')
        result = None
        if self.__class__._aead_decrypt_function:
            result = self.__class__._aead_decrypt_function(
                self._ciphertext, self._tag, header_bytes, self._nonce,
                self._jwk.k)
        elif self._header['alg'] == 'unsecured':
            if allow_unsecured is not True:
                raise RuntimeError('Access to unsecured (non-standard) JWE is'
                                   ' forbidden unless explicitly allowed.')
            if self._nonce or self._tag or self._key:
                raise RuntimeError('Unsecured (non-standard) JWEs must not'
                                   ' contain a key, tag or nonce.')

            result = self._ciphertext
        self._message_bytes = result
        self._message = utils.json_to_dict(result)
        return self._message


class ChaCha20Poly1305Jwe(SymmetricJwe):
    """
    ChaCha20/Poly1305 symmetric key encryption `C20P`.

    - https://tools.ietf.org/id/draft-amringer-jose-chacha-00.txt
    - RFC 7539 and RFC 8439.
    """

    _DEFAULT_HEADER = OrderedDict([('alg', 'dir'),
                                   ('enc', 'C20P')])
    _KEYBYTES = nacl_aead.KEYBYTES
    _NONCEBYTES = nacl_aead.NONCEBYTES
    _aead_encrypt_function = nacl_aead.chacha20poly1305_encrypt
    _aead_decrypt_function = nacl_aead.chacha20poly1305_decrypt


class AES256GCMJwe(SymmetricJwe):
    """
    AES-256-GCM symmetric key encryption `A256GCM`.
    """

    _DEFAULT_HEADER = OrderedDict([('alg', 'dir'),
                                   ('enc', 'A256GCM')])
    _KEYBYTES = cryptography_aead.KEYBYTES
    _NONCEBYTES = cryptography_aead.NONCEBYTES
    _aead_encrypt_function = cryptography_aead.aes256gcm_encrypt
    _aead_decrypt_function = cryptography_aead.aes256gcm_decrypt


class UnsecuredJwe(SymmetricJwe):
    """
    Non-standard JWE object that is unsecured (not encrypted).
    """

    _DEFAULT_HEADER = OrderedDict([('alg', 'unsecured')])
    _KEYBYTES = None
    _NONCEBYTES = None
    _aead_encrypt_function = None
    _aead_decrypt_function = None


class X25519Jwe(Jwe):
    """
    X25519 public key encryption base class.

    Creating an RFC 7518 ECDH-ES key derivation of a suitable key as in RFC
    8037. This is a base class, that requires implementation of the payload
    encryption using a symmetric cipher.

    - RFC 7539
    """

    _DEFAULT_HEADER = None  # type: Optional[dict]
    _KEYBYTES = 0  # type: Optional[int]
    _NONCEBYTES = 0  # type: Optional[int]
    _aead_encrypt_function = None  # type: Optional[Callable]
    _aead_decrypt_function = None  # type: Optional[Callable]

    def ecdh_es_key(self, full_key: X25519Jwk, public_key: X25519Jwk,
                    *, apu: bytes = b'', apv: bytes = b'') -> bytes:
        """
        Compute and return the shared key for a symmetric JWE encryption.

        The payload is encrypted. This requires ephemeral sender and
        recipient JWK keys.

        Thi KDF uses the shared DH secret and various 'input parameters' as
        described in RFC 7518 (Sect. 4.6 and Appendix C), implementing the
        NIST Special Publication 800-56A, Revision 2 (May 2013, Sect. 5.8):

        - https://tools.ietf.org/html/rfc7518
        - http://dx.doi.org/10.6028/NIST.SP.800-56Ar2

        :param full_key: First (private) JWK.
        :param public_key: Second (public) JWK.
        :param apu: Agreement PartyUInfo is producer information
            (optional, default: b'').
        :param apv: Agreement PartyVInfo is recipient information
            (optional, default: b'').
        :return: Binary encryption key of required length.
        """
        # Prepare data needed for key derivation function (KDF).
        public_dh_key = public_key._dh_key
        if isinstance(public_dh_key, nacl.public.PrivateKey):
            public_dh_key = public_dh_key.public_key
        a_box = nacl.public.Box(full_key._dh_key, public_dh_key)
        shared_secret = a_box.shared_key()
        algorithm_id = self._DEFAULT_HEADER['enc'].encode('utf-8')
        algorithm_id_length = _int_to_bytes(len(algorithm_id))
        apu_length = _int_to_bytes(len(apu))
        apv_length = _int_to_bytes(len(apv))
        keydata_length = _int_to_bytes(self._KEYBYTES << 3)  # In bits.
        # Assemble data and derive key via hashing-based KDF.
        other_info = (algorithm_id_length + algorithm_id
                      + apu_length + apu
                      + apv_length + apv
                      + keydata_length)
        round_number = _int_to_bytes(1)  # 1st (and only) round of hashing.
        hash_input = round_number + shared_secret + other_info
        derived_secret = nacl.hash.sha256(hash_input,
                                          encoder=nacl.encoding.RawEncoder)
        derived_key = derived_secret[:self._KEYBYTES]
        return derived_key

    def encrypt(self, *, apu: bytes = b'', apv: bytes = b'') -> (bytes, bytes):
        """
        Encrypt the JWE message, and store the resulting ciphertext and tag.

        :param apu: Agreement PartyUInfo is producer information
            (optional, default: b'').
        :param apv: Agreement PartyVInfo is recipient information
            (optional, default: b'').
        :return: Tuple (ciphertext, tag).
        """
        plaintext = self.get_message_bytes()
        self._header = self._DEFAULT_HEADER.copy()
        ephemeral_key_pair = X25519Jwk(generate=True)
        symmetric_key = self.ecdh_es_key(ephemeral_key_pair, self._jwk,
                                         apu=apu, apv=apv)
        if apu:
            self._header['apu'] = utils.bytes_to_string(apu)
        if apv:
            self._header['apv'] = utils.bytes_to_string(apv)
        self._header['epk'] = ephemeral_key_pair.to_dict(exclude_private=True)
        header_bytes = utils.dict_to_base64(self._header).encode('utf-8')
        self._nonce = nacl.utils.random(self._NONCEBYTES)
        result = self.__class__._aead_encrypt_function(
            plaintext, header_bytes, self._nonce, symmetric_key)
        self._ciphertext, self._tag = result
        return result

    def decrypt(self) -> bytes:
        """
        Decrypts the JWE ciphertext and stores the resulting message.

        :return: Decrypted message.
        """
        ephemeral_key = X25519Jwk(from_dict=self._header['epk'])
        apu = utils.string_to_bytes(self._header.get('apu', ''))
        apv = utils.string_to_bytes(self._header.get('apv', ''))
        symmetric_key = self.ecdh_es_key(self._jwk, ephemeral_key,
                                         apu=apu, apv=apv)
        header_bytes = utils.dict_to_base64(self._header).encode('utf-8')
        result = self.__class__._aead_decrypt_function(
            self._ciphertext, self._tag, header_bytes, self._nonce,
            symmetric_key)
        self._message_bytes = result
        self._message = utils.json_to_dict(result)
        return self._message


class X25519ChaCha20Poly1305Jwe(X25519Jwe):
    """
    X25519 public key encryption with ChaCha20/Poly1305 for the payload.

    Creating an RFC 7518 ECDH-ES key derivation of a suitable key as in RFC
    8037. Payload content is encrypted using ChaCha20/Poly1305 again.

    - https://tools.ietf.org/id/draft-amringer-jose-chacha-00.txt
    - RFC 7539 and RFC 8439
    """

    _DEFAULT_HEADER = OrderedDict([('alg', 'ECDH-ES'),
                                   ('enc', 'C20P'),
                                   ('epk', None)])
    _KEYBYTES = nacl_aead.KEYBYTES
    _NONCEBYTES = nacl_aead.NONCEBYTES
    _aead_encrypt_function = nacl_aead.chacha20poly1305_encrypt
    _aead_decrypt_function = nacl_aead.chacha20poly1305_decrypt


class X25519AES256GCMJwe(X25519Jwe):
    """
    X25519 public key encryption with AES256-GCM for the payload.

    Creating an RFC 7518 ECDH-ES key derivation of a suitable key as in RFC
    8037. Payload content is encrypted using AES256-GCM.

    - RFC 7539 and RFC 8439
    """

    _DEFAULT_HEADER = OrderedDict([('alg', 'ECDH-ES'),
                                   ('enc', 'A256GCM'),
                                   ('epk', None)])
    _KEYBYTES = cryptography_aead.KEYBYTES
    _NONCEBYTES = cryptography_aead.NONCEBYTES
    _aead_encrypt_function = cryptography_aead.aes256gcm_encrypt
    _aead_decrypt_function = cryptography_aead.aes256gcm_decrypt


_CLASS_MAPPING = {
    (ChaCha20Poly1305Jwe._DEFAULT_HEADER['enc'],
     ChaCha20Poly1305Jwe._DEFAULT_HEADER['alg']):
    ChaCha20Poly1305Jwe,
    (AES256GCMJwe._DEFAULT_HEADER['enc'],
     AES256GCMJwe._DEFAULT_HEADER['alg']):
    AES256GCMJwe,
    (UnsecuredJwe._DEFAULT_HEADER.get('enc'),
     UnsecuredJwe._DEFAULT_HEADER['alg']):
    UnsecuredJwe,
    (X25519ChaCha20Poly1305Jwe._DEFAULT_HEADER['enc'],
     X25519ChaCha20Poly1305Jwe._DEFAULT_HEADER['alg']):
    X25519ChaCha20Poly1305Jwe,
    (X25519AES256GCMJwe._DEFAULT_HEADER['enc'],
     X25519AES256GCMJwe._DEFAULT_HEADER['alg']):
    X25519AES256GCMJwe
}
