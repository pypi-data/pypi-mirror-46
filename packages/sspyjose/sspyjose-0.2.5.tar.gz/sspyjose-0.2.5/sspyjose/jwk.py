# -*- coding: utf-8 -*-
"""JWK (JSON Web Key) module for the JOSE package."""

# Created: 2018-07-20 Guy K. Kloss <guy@mysinglesource.io>
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

from collections import OrderedDict
import copy
import nacl.bindings
from typing import Iterable, Union, Optional

import nacl.public
import nacl.signing
from sspyjose import Jose
from sspyjose import cryptography_aead_wrap
from sspyjose import nacl_aead_wrap
from sspyjose import utils


class Jwk(Jose):
    """
    JSON Web Key (JWK) RFC 7517.

    Only implements key types for the following cipher suites:

    - ChaCha20/Poly1305 - 256-bit key size, 96-bit nonce
    - AES256-GCM - 256-bit key size, 96-bit nonce
    - X25519 - 256-bit key size
    - Ed25519 - 256-bit key (EdDSA with 256-bit key seed)

    Additional key information can be set within ``private`` data attributes
    (prefixed with an underscore ``_``), which will not be subject to
    serialisation.
    """

    _JSON_PRIVATE_KEY_ELEMENTS = None  # type: Optional[Iterable]
    """Elements of the key containing secrets."""
    _JSON_BINARY_ELEMENTS = None  # type: Optional[Iterable]
    """Elements of the key containing binary data."""

    def __init__(self, kty: str):
        """
        Constructor.

        :param kty: Key type.
        """
        super().__init__()
        self._data['kty'] = kty

    @classmethod
    def get_instance(
            cls, *,
            alg: Optional[str] = None,
            crv: Optional[str] = None,
            from_json: Optional[str] = None,
            from_dict: Optional[dict] = None,
            generate: bool = False,
            from_secret: Union[str, bytes, None] = None) -> 'Jwk':
        """
        Get an instance of a specific JWK object by algorithm via factory.

        :param alg: Specific encryption algorithm indicator (default: None).
        :param crv: Elliptic curve to use for the public key algorithm
            (default: None).
        :param from_json: Initialise the key from the given JSON
            representation of JWK key content (default: None).
        :param from_dict: Initialise the key from the given dictionary
            representation of JWK key content (equivalent content to JSON,
            default: None).
        :param generate: Generate a new key (default: False).
        :param from_secret: From the secret key (default: None). Only
            applicable to symmetric keys!
        :return: A {Jwk} object or `None` if no suitable class is available.
        """
        if alg is None and crv is None:
            if from_dict:
                alg = from_dict.get('alg')
                crv = from_dict.get('crv')
            elif from_json:
                content = utils.json_to_dict(from_json)
                alg = content.get('alg')
                crv = content.get('crv')
        if alg is None and crv is None:
            # Still nothing, set the default.
            alg = Jose.DEFAULT_ENC
        klass = _CLASS_MAPPING.get((alg, crv))
        if klass:
            if (from_secret
                    and alg in [ChaCha20Poly1305Jwk._DEFAULT_HEADER['alg'],
                                AES256GCMJwk._DEFAULT_HEADER['alg']]):
                return klass(from_json=from_json, from_dict=from_dict,
                             generate=generate, from_secret=from_secret)
            else:
                return klass(from_json=from_json, from_dict=from_dict,
                             generate=generate)
        raise RuntimeError(
            'No suitable JWK type implemented for alg={} and crv={}.'
            .format(alg, crv))

    @property
    def kty(self) -> str:
        """Key type."""
        return self._data['kty']

    @property
    def kid(self) -> str:
        """Key ID."""
        return self._data.get('kid')

    def to_dict(self, exclude_private: bool = False) -> dict:
        """
        Express the JWK as a JOSE compliant dictionary.

        :param exclude_private: Optional parameter to exclude private key
            information in the JSON serialisation.
        :return: Dictionary representation of key.
        """
        to_remove = (self._JSON_PRIVATE_KEY_ELEMENTS
                     if exclude_private else None)
        return utils.pack_bytes(self._data, to_remove)

    def to_json(self, exclude_private: bool = False) -> str:
        """
        Serialise the JWK to JOSE compliant JSON.

        :param exclude_private: Optional parameter to exclude private key
            information in the JSON serialisation.
        :return: JSON string of key.
        """
        to_remove = (self._JSON_PRIVATE_KEY_ELEMENTS
                     if exclude_private else None)
        return utils.dict_to_json(self._data, to_remove)

    @property
    def json(self) -> str:
        """Serialise JWK as JOSE compliant JSON."""
        return self.to_json()

    def generate_key(self):
        """Generate a new key pair for this JWK object."""
        raise NotImplementedError('Needs to be implemented by child class.')

    def from_json(self, content: str):
        """
        Load a new key from JSON content into this JWK object.

        :param content: JSON representation of JWK key content.
        """
        raise NotImplementedError('Needs to be implemented by child class.')

    def from_dict(self, content: dict):
        """
        Load a new key from JSON content into this JWK object.

        :param content: Dictionary representation of JWK key content.
        """
        raise NotImplementedError('Needs to be implemented by child class.')


class Ed25519Jwk(Jwk):
    """
    Edwards 25519 EdDSA signing key.
    """

    _JSON_PRIVATE_KEY_ELEMENTS = ('d',)
    _JSON_BINARY_ELEMENTS = ('x', 'd')
    _DEFAULT_HEADER = OrderedDict([('crv', 'Ed25519')])
    _signing_key = None  # type: Optional[nacl.signining.SigningKey]
    """PyNaCl signing key (private seed)."""
    _verify_key = None  # type: Optional[nacl.signining.VerifyKey]
    """PyNaCl verify key (public)."""

    def __init__(self, *,
                 from_json: Optional[str] = None,
                 from_dict: Optional[dict] = None,
                 generate: bool = False):
        """
        Constructor.

        :param from_json: Initialise the key from the given JSON
            representation of JWK key content (default: None).
        :param from_dict: Initialise the key from the given dictionary
            representation of JWK key content (equivalent content to JSON,
            default: None).
        :param generate: Generate a new key pair (default: False).
        """
        super().__init__('OKP')
        self._data.update(self._DEFAULT_HEADER)
        if from_json and generate:
            raise ValueError('Only one key generation method can be given.')
        if from_json:
            self.from_json(from_json)
        if from_dict:
            self.from_dict(from_dict)
        elif generate:
            self.generate_key()

    def generate_key(self):
        """Generate a new key pair for this JWK object."""
        signing_key = nacl.signing.SigningKey.generate()
        d = bytes(signing_key)
        x = bytes(signing_key.verify_key)
        self._data['d'] = d
        self._data['x'] = x
        self._data['_signing_key'] = signing_key

    def from_json(self, content: str):
        """
        Load a new key from JSON content into this JWK object.

        :param content: JSON representation of JWK key content.
        """
        self._data = utils.json_to_dict(
            content, binary=self._JSON_BINARY_ELEMENTS)

    def from_dict(self, content: dict):
        """
        Load a new key from JSON content into this JWK object.

        :param content: Dictionary representation of JWK key content.
        """
        content = copy.deepcopy(content)
        self._data = content
        if isinstance(self._data['x'], str):
            self._data['x'] = utils.string_to_bytes(content['x'])
        new_x = self._data['x']
        if 'd' in content and isinstance(content['d'], str):
            self.d = content['d']
            # Constant time hash comparison (do not use `!=` or `==`).
            if not nacl.bindings.sodium_memcmp(self._data['x'], new_x):
                raise RuntimeError(
                    'Public key `x` does not match `x` computed from'
                    ' private key `d`.')

    @property
    def crv(self) -> str:
        """Elliptic curve type."""
        return self._data['crv']

    @property
    def x(self) -> bytes:
        """Public key."""
        return self._data['x']

    @x.setter
    def x(self, value: Union[bytes, str]):
        """
        Set public key.

        :param value: Value of the public key. If a string is passed in, it
            will be decoded using URL safe base64 encoding.
        """
        pubkey = None
        if isinstance(value, bytes):
            pubkey = value
        elif isinstance(value, str):
            pubkey = utils.string_to_bytes(value)
        else:
            raise ValueError('Public key to set must be `bytes` or `str`.')
        if len(pubkey) != nacl.bindings.crypto_sign_PUBLICKEYBYTES:
            raise ValueError('Public key must be exactly {} bytes in size.'
                             .format(nacl.bindings.crypto_sign_PUBLICKEYBYTES))
        self._data['x'] = pubkey

    @property
    def d(self) -> bytes:
        """Private key seed."""
        return self._data.get('d')

    @d.setter
    def d(self, value: Union[bytes, str]):
        """
        Set signing key seed.

        :param value: Value of the key seed. If a string is passed in, it
            will be decoded using URL safe base64 encoding.
        """
        key_seed = None
        if isinstance(value, bytes):
            key_seed = value
        elif isinstance(value, str):
            key_seed = utils.string_to_bytes(value)
        else:
            raise ValueError('Key seed to set must be `bytes` or `str`.')
        if len(key_seed) != nacl.bindings.crypto_sign_SEEDBYTES:
            raise ValueError('Key seed must be exactly {} bytes in size.'
                             .format(nacl.bindings.crypto_sign_SEEDBYTES))
        self._data['d'] = key_seed
        signing_key = nacl.signing.SigningKey(key_seed)
        self._data['_signing_key'] = signing_key
        self._data['x'] = bytes(signing_key.verify_key)

    @property
    def _signing_key(self):
        """Signing key object for PyNaCl."""
        if '_signing_key' not in self._data:
            signing_key = nacl.signing.SigningKey(self._data['d'])
            self._data['_signing_key'] = signing_key
        return self._data['_signing_key']

    @property
    def _verify_key(self):
        """Verify key object for PyNaCl."""
        if '_verify_key' not in self._data:
            verify_key = nacl.signing.VerifyKey(self._data['x'])
            self._data['_verify_key'] = verify_key
        return self._data['_verify_key']


class X25519Jwk(Jwk):
    """X25519 Diffie-Hellman key."""

    _JSON_PRIVATE_KEY_ELEMENTS = ('d',)
    _JSON_BINARY_ELEMENTS = ('x', 'd')
    _DEFAULT_HEADER = OrderedDict([('crv', 'X25519')])
    _dh_key = None  # type: Optional[nacl.public.PrivateKey]
    """PyNaCl Diffie-Hellman key (private)."""

    def __init__(self, *,
                 from_json: Optional[str] = None,
                 from_dict: Optional[dict] = None,
                 generate: bool = False):
        """
        Constructor.

        :param from_json: Initialise the key from the given JSON
            representation of JWK key content (default: None).
        :param from_dict: Initialise the key from the given dictionary
            representation of JWK key content (equivalent content to JSON,
            default: None).
        :param generate: Generate a new key pair (default: False).
        """
        super().__init__('OKP')
        self._data.update(self._DEFAULT_HEADER)
        if from_json and generate:
            raise ValueError('Only one key generation method can be given.')
        if from_json:
            self.from_json(from_json)
        if from_dict:
            self.from_dict(from_dict)
        elif generate:
            self.generate_key()

    def generate_key(self):
        """Generate a new key pair for this JWK object."""
        my_key = nacl.public.PrivateKey.generate()
        d = bytes(my_key)
        x = bytes(my_key.public_key)
        self._data['d'] = bytes(d)
        self._data['_dh_key'] = my_key
        self._data['x'] = x

    def from_json(self, content: str):
        """
        Load a new key from JSON content into this JWK object.

        :param content: JSON representation of JWK key content.
        """
        self._data = utils.json_to_dict(
            content, binary=self._JSON_BINARY_ELEMENTS)

    def from_dict(self, content: dict):
        """
        Load a new key from JSON content into this JWK object.

        :param content: Dictionary representation of JWK key content.
        """
        content = copy.deepcopy(content)
        self._data = content
        if isinstance(self._data['x'], str):
            self._data['x'] = utils.string_to_bytes(content['x'])
        new_x = self._data['x']
        if 'd' in content and isinstance(content['d'], str):
            self.d = content['d']
            # Constant time hash comparison (do not use `!=` or `==`).
            if not nacl.bindings.sodium_memcmp(self._data['x'], new_x):
                raise RuntimeError(
                    'Public key `x` does not match `x` computed from'
                    ' private key `d`.')

    @property
    def crv(self) -> str:
        """Elliptic curve type."""
        return self._data['crv']

    @property
    def x(self) -> bytes:
        """Public key."""
        return self._data['x']

    @property
    def d(self) -> bytes:
        """Private key."""
        return self._data['d']

    @d.setter
    def d(self, value: Union[bytes, str]):
        """
        Set private key.

        :param value: Value of the private key. If a string is passed in, it
            will be decoded using URL safe base64 encoding.
        """
        private_key = None
        if isinstance(value, bytes):
            private_key = value
        elif isinstance(value, str):
            private_key = utils.string_to_bytes(value)
        else:
            raise ValueError('Private key to set must be `bytes` or `str`.')
        if len(private_key) != nacl.public.PrivateKey.SIZE:
            raise ValueError('Private key must be exactly {} bytes in size.'
                             .format(nacl.public.PrivateKey.SIZE))
        my_key = nacl.public.PrivateKey(private_key)
        self._data['d'] = private_key
        self._data['_dh_key'] = my_key
        self._data['x'] = bytes(my_key.public_key)

    @property
    def _dh_key(self):
        """Diffie-Hellman key object for PyNaCl."""
        if '_dh_key' not in self._data:
            if 'd' in self._data:
                dh_key = nacl.public.PrivateKey(self._data['d'])
            else:
                dh_key = nacl.public.PublicKey(self._data['x'])
            self._data['_dh_key'] = dh_key
        return self._data['_dh_key']


class SymmetricJwk(Jwk):
    """Symmetric key."""

    _JSON_PRIVATE_KEY_ELEMENTS = ('k',)
    _JSON_BINARY_ELEMENTS = ('k',)
    _DEFAULT_HEADER = None  # type: Optional[dict]
    _KEY_SIZE = None  # type: Optional[int]

    def __init__(self, *,
                 from_json: Optional[str] = None,
                 from_dict: Optional[dict] = None,
                 from_secret: Union[str, bytes, None] = None,
                 generate: bool = False):
        """
        Constructor.

        :param from_json: Initialise the key from the given JSON
            representation of JWK key content (default: None).
        :param from_dict: Initialise the key from the given dictionary
            representation of JWK key content (equivalent content to JSON,
            default: None).
        :param from_secret: From the secret key.
        :param generate: Generate a new key (default: False).
        """
        super().__init__('oct')
        self._data.update(self._DEFAULT_HEADER)
        if generate and (from_json or from_dict or from_secret):
            raise ValueError('Only one key generation method can be given.')
        if generate:
            self.generate_key()
        elif from_json:
            self.from_json(from_json)
        elif from_dict:
            self.from_dict(from_dict)
        elif from_secret:
            if isinstance(from_secret, str):
                from_secret = utils.string_to_bytes(from_secret)
            self._data['k'] = from_secret

    def generate_key(self):
        """Generate a new key for this JWK object."""
        self._data['k'] = nacl.utils.random(self._KEY_SIZE)

    def from_json(self, content: str):
        """
        Load a new key from JSON content into this JWK object.

        :param content: JSON representation of JWK key content.
        """
        self._data = utils.json_to_dict(
            content, binary=self._JSON_BINARY_ELEMENTS)

    def from_dict(self, content: dict):
        """
        Load a new key from JSON content into this JWK object.

        :param content: Dictionary representation of JWK key content.
        """
        content = copy.deepcopy(content)
        if isinstance(content['k'], str):
            content['k'] = utils.string_to_bytes(content['k'])
        self._data = content

    @property
    def k(self) -> bytes:
        """Encryption key."""
        return self._data['k']

    @k.setter
    def k(self, value: Union[bytes, str]):
        """
        Set encryption key.

        :param value: Value of the key. If a string is passed in, it will be
            decoded using URL safe base64 encoding.
        """
        key = None
        if isinstance(value, bytes):
            key = value
        elif isinstance(value, str):
            key = utils.string_to_bytes(value)
        else:
            raise ValueError('Key to set must be `bytes` or `str`.')
        if len(key) != self._KEY_SIZE:
            raise ValueError('Key must be exactly {} bytes in size.'
                             .format(self._KEY_SIZE))
        self._data['k'] = key

    @property
    def alg(self) -> str:
        """Encryption algorithm (`alg` attribute)."""
        return self._data['alg']

    @property
    def use(self) -> str:
        """Key usage."""
        return self._data['use']


class ChaCha20Poly1305Jwk(SymmetricJwk):
    """ChaCha20/Poly1305 symmetric key."""

    _DEFAULT_HEADER = OrderedDict([('alg', 'C20P'),
                                   ('use', 'enc')])
    _KEY_SIZE = nacl_aead_wrap.KEYBYTES


class AES256GCMJwk(SymmetricJwk):
    """AES256-GCM symmetric key."""

    _DEFAULT_HEADER = OrderedDict([('alg', 'A256GCM'),
                                   ('use', 'enc')])
    _KEY_SIZE = cryptography_aead_wrap.KEYBYTES


_CLASS_MAPPING = {
    (ChaCha20Poly1305Jwk._DEFAULT_HEADER['alg'], None): ChaCha20Poly1305Jwk,
    (AES256GCMJwk._DEFAULT_HEADER['alg'], None): AES256GCMJwk,
    (None, Ed25519Jwk._DEFAULT_HEADER['crv']): Ed25519Jwk,
    (None, X25519Jwk._DEFAULT_HEADER['crv']): X25519Jwk
}
