# -*- coding: utf-8 -*-
"""JSON Object signing and Encryption (JOSE, RFC 7520) base."""

# Created: 2018-07-25 Guy K. Kloss <guy@mysinglesource.io>
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


class Jose:
    """
    JSON Object signing and Encryption (JOSE, RFC 7520) base class.

    JOSE is split into 5 main components:

    - JSON Web Algorithms (JWA, RFC 7518).
    - JSON Web Encryption (JWE, RFC 7516).
    - JSON Web Key (JWK, RFC 7517).
    - JSON Web Signature (JWS, RFC 7515).
    - JSON Web Token (JWT, RFC 7519).

    Additional specifications and drafts implemented:

    - ChaCha20/Poly1305 JWE symmetric key encryption (RFC 7539).
    - Ed25519 JWS signature (RFC 8037).
    - JSON Web Key (JWK) Thumbprint (RFC 7638).
    - JWS Unencoded Payload Option (RFC 7797).

    We need JWK, JWE and JWS.
    """

    DEFAULT_ENC = 'C20P'
    """Default cipher for symmetric encryption."""
    DEFAULT_SIG = 'Ed25519'
    """Default cipher for cryptographic signatures."""
    _data = None  # type: dict
    """JOSE object data."""

    def __init__(self):
        """Constructor."""
        self._data = {}

    def to_json(self):  # noqa: D102
        raise NotImplementedError('Needs to be implemented by child class.')

    @staticmethod
    def from_json(content):  # noqa: D102
        raise NotImplementedError('Needs to be implemented by child class.')
