# -*- coding: utf-8 -*-
"""Functional utilities."""

# Created: 2018-07-24 Guy K. Kloss <guy@mysinglesource.io>
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
import re
from typing import Iterable, Union, Optional

_NUMBER_TEST = re.compile(r'^[0-9]+$')


def bytes_to_string(value: bytes) -> str:
    """
    Convert `bytes` to a base64 URL encoded string.

    Trailing padding characters (`=`) are stripped.

    :param value: Bytes to be converted.
    :return: String representation.
    """
    return base64.urlsafe_b64encode(value).strip(b'=').decode('utf-8')


def string_to_bytes(value: str) -> bytes:
    """
    Convert base64 URL encoded string to `bytes`.

    Trailing padding characters (`=`) are added.

    :param value: String representation.
    :return: Bytes representation.
    """
    return base64.urlsafe_b64decode(value.encode('utf-8') + b'==')


def _transform_simple(data):
    """Transform a simple data type (not an iterable) for serialisation."""
    if isinstance(data, bytes):
        return bytes_to_string(data)
    else:
        return data


def pack_bytes(data: dict, to_remove: Optional[Iterable[str]] = None) -> dict:
    """
    Convert `bytes` in a dictionary to a copy with base64 URL strings.

    Objects elements with a key starting with an underscore ``_``
    are considered "private" are stripped out.

    :param data: JSON data as a dictionary.
    :param to_remove: Optionally object attributes to remove from
        serialisation (default: None).
    :return: Binary converted dictionary representation of JOSE data.
    """
    if not isinstance(data, dict):
        return _transform_simple(data)
    result = OrderedDict()
    to_remove = to_remove or []
    for key, value in data.items():
        if isinstance(key, str) and _NUMBER_TEST.match(key):
            key = int(key)
        if isinstance(key, str) and (key.startswith('_') or key in to_remove):
            continue
        elif isinstance(value, dict):
            result[key] = pack_bytes(value, to_remove)
        elif isinstance(value, (list, tuple)):
            result[key] = [pack_bytes(item, to_remove)
                           for item in value]
        else:
            result[key] = _transform_simple(value)
    return result


def unpack_bytes(data: dict, binary: Optional[Iterable[str]] = None) -> dict:
    """
    Convert base64 URL encoded strings in a JOSE dictionary to `bytes`.

    :param data: JSON data as a dictionary.
    :param binary: Optionally an iterable of strings for elements that
        must be converted from a base64 URL encoded representation
        into bytes.
    :return: Binary converted dictionary representation of JOSE data.
    """
    binary = binary or []
    for key, value in data.items():
        if isinstance(value, dict):
            data[key] = unpack_bytes(value, binary)
        elif isinstance(value, str) and key in binary:
            data[key] = string_to_bytes(value)
    return data


def dict_to_json(data: dict, to_remove: Optional[Iterable[str]] = None) -> str:
    """
    Convert a JOSE representation of a JOSE object to JSON representation.

    All binary data (bytes) will be base64 URL encoded. Objects elements
    with a key starting with an underscore ``_`` are considered "private"
    are stripped out.

    :param data: Python dictionary representation of JOSE data.
    :param to_remove: Optionally object attributes to remove from
        serialisation (default: None).
    :return: JSON encoded data.
    """
    return json.dumps(pack_bytes(data, to_remove),
                      indent=None, separators=(',', ':'))


def json_to_dict(data: Union[str, bytes],
                 binary: Optional[Iterable[str]] = None) -> dict:
    """
    Convert a JSON representation of a JOSE object to a Python dict.

    :param data: JSON encoded data.
    :param binary: Optionally an iterable of strings for elements that
        must be converted from a base64 URL encoded representation
        into bytes.
    :return: Python dictionary representation of JOSE data.
    """
    return unpack_bytes(json.loads(data, object_pairs_hook=OrderedDict),
                        binary)


def dict_to_base64(data: dict,
                   to_remove: Optional[Iterable[str]] = None) -> str:
    """
    Convert a JOSE dict to a URL-safe base64 representation of a JSON string.

    All binary data (bytes) will be base64 URL encoded. Objects elements
    with a key starting with an underscore ``_`` are considered "private"
    are stripped out.

    :param data: Python dictionary representation of JOSE data.
    :param to_remove: Optionally object attributes to remove from
        serialisation (default: None).
    :return: Encoded string representation.
    """
    json_form = json.dumps(pack_bytes(data, to_remove),
                           indent=None, separators=(',', ':'))
    return bytes_to_string(json_form.encode('utf-8'))


def base64_to_dict(data: str, binary: Optional[Iterable[str]] = None) -> dict:
    """
    Convert a URL base64 representation of a JSON string to a `dict`.

    :param data: Base64 string representation of JOSE data.
    :param binary: Optionally an iterable of strings for elements that
        must be converted from a base64 URL encoded representation
        into bytes.
    :return: Dictionary representation.
    """
    json_form = string_to_bytes(data)
    return json_to_dict(json_form, binary)
