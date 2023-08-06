# -*- coding: utf-8 -*-
"""JWS (JSON Web Signature) module for the JOSE package."""

# Created: 2018-08-01 Guy K. Kloss <guy@mysinglesource.io>
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
import json
from typing import Union, List, Optional

import nacl.hash
from sspyjose import Jose
from sspyjose import utils
from sspyjose.jwk import Jwk


class Jws(Jose):
    """
    JSON Web Signature (JWK) RFC 7515.

    Only implements the following cipher suites:

    - Ed25519 - public key-based, 256-bit key size (RFC 8037).
    """

    _header = None  # type: Optional[dict]
    """Protected (signed) header."""
    _payload = None  # type: Optional[dict]
    """Payload (signed)."""
    _signature = None  # type: Optional[bytes]
    """Signature."""
    _jwk = None  # type: Union[bytes, list[bytes], None]
    """Signing key."""
    _SERIALISATION_PARTS = ('header', 'payload', 'signature')
    """Parts of the JWS compact serialisation specification."""
    _DEFAULT_HEADER = OrderedDict()
    """Default header to use for this JWS type."""

    def __init__(self, *,
                 from_compact: Union[bytes, str, None] = None,
                 from_json: Union[bytes, str, None] = None,
                 jwk: Jwk = None):
        """
        Constructor.

        :param from_compact: If present, load data from compact ASCII JWS
            serialisation format.
        :param from_json: If present, load data from JSON JWS
            serialisation format. This form is to be used for
            multi-signature JWS objects.
        :param jwk: JWK to use for signing/validating.
        """
        super().__init__()
        self._header = self._DEFAULT_HEADER.copy()
        if from_compact:
            self.load_compact(from_compact)
        if from_json:
            self.load_json(from_json)
        if jwk:
            self._jwk = jwk

    @classmethod
    def get_instance(
            cls, *,
            alg: Optional[str] = None,
            from_compact: Union[bytes, str, None] = None,
            from_json: Union[bytes, str, None] = None,
            jwk: Optional[Jwk] = None) -> 'Jws':
        """
        Get an instance of a specific JWS object by algorithm via factory.

        :param alg: Specific algorithm indicator
            (default: {Jose.DEFAULT_SIG}).
        :param from_compact: Load data from compact ASCII JWS serialisation
            format (default: None).
        :param from_json: Load data from JSON JWS serialisation format
            (default: None). This form is to be used for multi-signature JWS
            objects.
        :param jwk: JWK to use for signing/verifying (default: None).
        :return: A {Jws} object.
        """
        if alg is None:
            alg = Jose.DEFAULT_SIG
        klass = _CLASS_MAPPING.get(alg)
        if klass:
            return klass(from_compact=from_compact, from_json=from_json,
                         jwk=jwk)
        raise RuntimeError('No suitable JWS type implemented for alg={}.'
                           .format(alg))

    @property
    def header(self) -> dict:
        """Protected header."""
        return self._header

    @header.setter
    def header(self, value: dict):
        """
        Set the protected header. This clears any signature attribute value.

        :param value: Content in bytes.
        """
        self._header = value
        self._signature = None

    @property
    def payload(self) -> dict:
        """Plain text message."""
        return self._payload

    @payload.setter
    def payload(self, value: dict):
        """
        Set payload to sign. This clears any signature attribute value.

        :param value: Content in bytes.
        """
        self._payload = value
        self._signature = None

    def _get_message(self) -> bytes:
        """Bytes of message and protected header to sign/validate."""
        header = utils.dict_to_base64(self._header).encode('utf-8')
        payload = utils.dict_to_base64(self._payload).encode('utf-8')
        return b'.'.join([header, payload])

    @property
    def signature(self) -> Union[bytes, List[bytes]]:
        """Signature."""
        return self._signature

    @signature.setter
    def signature(self, value: Union[bytes, List[bytes]]):
        """
        Set signature.

        :param value: Content in bytes.
        """
        self._signature = value

    @property
    def jwk(self) -> Jwk:
        """Signing/validating key for this JWS."""
        return self._jwk

    @jwk.setter
    def jwk(self, value: Jwk):
        """
        Set signing/validating key for this JWS.

        :param value: JWK key object.
        """
        self._jwk = value

    def add_jwk(self, value: Jwk):
        """
        Set signing/validating key for this JWS.

        :param value: JWK key object.
        """
        if self._jwk is None:
            self._jwk = value
        elif not isinstance(self._jwk, list):
            self._jwk = [self._jwk]
            self._jwk.append(value)
        else:
            self._jwk.append(value)

    def to_dict(self) -> dict:
        """Serialise to a dictionary for further string serialisation."""
        result = OrderedDict()
        if isinstance(self._signature, list):
            result['payload'] = utils.dict_to_base64(self._payload)
            result['signatures'] = []
            for key, signature in zip(self._jwk, self._signature):
                part = OrderedDict()
                part['protected'] = utils.dict_to_base64(self._header)
                header = {}
                if key.kid:
                    header['kid'] = key.kid
                else:
                    header['key_hash'] = nacl.hash.sha256(
                        key.x, encoder=nacl.encoding.RawEncoder)
                part['header'] = header
                part['signature'] = signature
                result['signatures'].append(part)
        else:
            for item in self._SERIALISATION_PARTS:
                part = getattr(self, '_' + item)
                if isinstance(part, dict):
                    part = utils.dict_to_base64(part)
                elif isinstance(part, bytes):
                    part = utils.bytes_to_string(part)
                elif part is None:
                    part = ''
                result[item] = part
        return result

    def to_json(self) -> str:
        """
        Serialise the JWS to JOSE compliant JSON.
        """
        return utils.dict_to_json(self.to_dict())

    def serialise(self, try_compact: bool = True) -> str:
        """
        Serialise the JWS.

        :param try_compact: Try the compact serialisation, if possible
            (default: True).
        :return: Serialised JWS.
        """
        if not try_compact or isinstance(self._signature, list):
            return self.to_json()
        base_serialised = self.to_dict()
        parts = [base_serialised[item]
                 for item in self._SERIALISATION_PARTS]
        return '.'.join(parts)

    @property
    def json(self) -> str:
        """Serialise JWS to JOSE compliant JSON."""
        return self.to_json()

    def load_compact(self, data: Union[bytes, str]):
        """
        Load JWS compact serialisation format.

        :param data: Serialisation data.
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        parts = data.split(b'.')
        if len(parts) != len(self._SERIALISATION_PARTS):
            raise ValueError(
                'Trying to load JWS compact serialisation with other than'
                ' {} parts: {} found.'
                .format(len(self._SERIALISATION_PARTS), len(parts)))
        parts = [base64.urlsafe_b64decode(item + b'==')
                 if item != b'' else None
                 for item in parts]
        content = dict(zip(self._SERIALISATION_PARTS, parts))
        content['header'] = json.loads(content['header'],
                                       object_pairs_hook=OrderedDict)
        content['payload'] = json.loads(content['payload'],
                                        object_pairs_hook=OrderedDict)
        for key, value in content.items():
            setattr(self, '_' + key, value)

    def load_json(self, data: Union[bytes, str]) -> List[dict]:
        """
        Load JWS JSON serialisation format.

        Note: Currently it is not possible to load multi-sig JWS with using
              different signing schemes/algorithms.

        :param data: Serialisation data.
        :return: List of the contained signatures' headers (containing e.g.
            the key IDs) in order of the signatures.
        """
        content = utils.json_to_dict(data)
        if set(content.keys()) != {'payload', 'signatures'}:
            raise ValueError('Got data incompatible with the form of JWS'
                             ' JSON serialisation for multi-signatures.')
        self._payload = utils.base64_to_dict(content['payload'])
        self._signature = []
        headers = []
        for signature in content['signatures']:
            headers.append(signature['header'])
            protected = utils.base64_to_dict(signature['protected'])
            if 'alg' not in self._header:
                self._header = protected
            elif protected['alg'] != self._header['alg']:
                raise RuntimeError(
                    'Object not suitable for loading a JWS {} signature'
                    ' into this {} object containing a {} signature.'
                    .format(protected['alg'], self.__class__,
                            self._header['alg']))
            # Need to 'binarise' the signature data, too
            self._signature.append(
                utils.string_to_bytes(signature['signature']))
        return headers

    def sign(self):
        """
        Sign the JWS payload and protected header.

        This also stores the resulting signature.
        """
        raise NotImplementedError('Needs to be implemented by child class.')

    def verify(self) -> bool:
        """
        Verify the JWS signature.

        :return: `True` on a valid signature.
        :raise: {nacl.exceptions.BadSignatureError} on an invalid signature.
        """
        raise NotImplementedError('Needs to be implemented by child class.')


class Ed25519Jws(Jws):
    """Ed25519 JWS signature (RFC 8037)."""

    _DEFAULT_HEADER = OrderedDict([('alg', 'Ed25519')])

    def sign(self):
        """
        Sign the JWS payload and protected header.

        This also stores the resulting signature.
        """
        if isinstance(self._jwk, list):
            self._signature = []
            for key in self._jwk:
                self._signature.append(
                    key._signing_key.sign(self._get_message()).signature)
        else:
            self._signature = (
                self._jwk._signing_key.sign(self._get_message()).signature)

    def verify(self) -> bool:
        """
        Verify the JWS signature.

        :return: `True` on a valid signature.
        :raise: {nacl.exceptions.BadSignatureError} on an invalid signature.
        """
        message = self._get_message()
        if (not isinstance(self._signature, list)
                and not isinstance(self._jwk, list)):
            self._jwk._verify_key.verify(message, signature=self._signature)
        else:
            no_keys = (1 if isinstance(self._jwk, Jwk)
                       else len(self._jwk))
            no_signatures = (1 if isinstance(self._signature, Jws)
                             else len(self._signature))
            if no_keys != no_signatures:
                raise nacl.exceptions.RuntimeError(
                    'Need {0} keys to verify {0} signatures, {1} given.'
                    .format(no_signatures, no_keys))
            message = self._get_message()
            for signature, jwk in zip(self._signature, self._jwk):
                jwk._verify_key.verify(message, signature=signature)
        return True


_CLASS_MAPPING = {
    Ed25519Jws._DEFAULT_HEADER['alg']: Ed25519Jws
}
