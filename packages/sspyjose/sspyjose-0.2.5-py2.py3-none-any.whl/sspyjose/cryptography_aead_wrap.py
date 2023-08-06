# -*- coding: utf-8 -*-
"""
Wrapper to Cryptography hazmat primitives bindings.

Exposes Authenticated Encryption with Associated Data (AEAD) compliant
en-/decryption using AES-GCM more cleanly.
"""

# Created: 2019-03-08 Guy K. Kloss <guy@mysinglesource.io>
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

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

KEYBYTES = 32
NONCEBYTES = 12
ABYTES = 16


def aes256gcm_encrypt(message: bytes, aad: bytes,
                      nonce: bytes, key: bytes) -> (bytes, bytes):
    """
    Encrypt the ``message`` using AEAD with AES256-GCM.

    :param message: Message to be encrypted.
    :param aad: Additional authenticated data.
    :param nonce: Nonce.
    :param key: Encryption key.
    :return: Tuple of (ciphertext, tag) bytes.
    """
    aesgcm = AESGCM(key)
    result = aesgcm.encrypt(nonce, message, aad)
    return result[:-ABYTES], result[-ABYTES:]


def aes256gcm_decrypt(ciphertext: bytes, tag: bytes, aad: bytes,
                      nonce: bytes, key: bytes) -> bytes:
    """
    Decrypt the ``ciphertext`` using AEAD with AES256-GCM.

    :param ciphertext: Message to be encrypted.
    :param tag: Authentication data (a MAC).
    :param aad: Additional authenticated data.
    :param nonce: Nonce.
    :param key: Encryption key.
    :return: Plaintext bytes.
    :raise: {cryptography.exceptions.InvalidTag} on an invalid tag.
    """
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext + tag, aad)
