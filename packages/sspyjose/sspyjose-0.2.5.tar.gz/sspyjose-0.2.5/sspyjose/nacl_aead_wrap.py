# -*- coding: utf-8 -*-
"""
Wrapper to PyNaCl raw bindings.

Exposes IETF Authenticated Encryption with Associated Data (AEAD) compliant
en-/decryption using ChaCha20/Poly1305 more cleanly.
"""

# Created: 2018-08-02 Guy K. Kloss <guy@mysinglesource.io>
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

from nacl.bindings import crypto_aead

KEYBYTES = crypto_aead.crypto_aead_chacha20poly1305_ietf_KEYBYTES
NONCEBYTES = crypto_aead.crypto_aead_chacha20poly1305_ietf_NPUBBYTES
ABYTES = crypto_aead.crypto_aead_chacha20poly1305_ietf_ABYTES


def chacha20poly1305_encrypt(message: bytes, aad: bytes,
                             nonce: bytes, key: bytes) -> (bytes, bytes):
    """
    Encrypt the ``message`` using the IETF ratified ChaCha20/Poly1305.

    According to RFC 7539.

    :param message: Message to be encrypted.
    :param aad: Additional authenticated data.
    :param nonce: Nonce.
    :param key: Encryption key.
    :return: Tuple of (ciphertext, tag) bytes.
    """
    result = crypto_aead.crypto_aead_chacha20poly1305_ietf_encrypt(
        message, aad, nonce, key)
    return result[:-ABYTES], result[-ABYTES:]


def chacha20poly1305_decrypt(ciphertext: bytes, tag: bytes, aad: bytes,
                             nonce: bytes, key: bytes) -> bytes:
    """
    Decrypt the ``ciphertext`` using the IETF ratified ChaCha20/Poly1305.

    According to RFC 7539.

    :param ciphertext: Message to be encrypted.
    :param tag: Authentication data (a MAC).
    :param aad: Additional authenticated data.
    :param nonce: Nonce.
    :param key: Encryption key.
    :return: Plaintext bytes.
    :raise: {nacl.exceptions.CryptoError} on an invalid tag.
    """
    return crypto_aead.crypto_aead_chacha20poly1305_ietf_decrypt(
        ciphertext + tag, aad, nonce, key)
