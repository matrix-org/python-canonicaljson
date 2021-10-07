# -*- coding: utf-8 -*-

# Copyright 2014 OpenMarket Ltd
# Copyright 2018 New Vector Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import platform

from frozendict import frozendict

__version__ = "1.5.0"


def _default(obj):  # pragma: no cover
    if type(obj) is frozendict:
        # fishing the protected dict out of the object is a bit nasty,
        # but we don't really want the overhead of copying the dict.
        try:
            return obj._dict
        except AttributeError:
            # When the C implementation of frozendict is used,
            # there isn't a `_dict` attribute with a dict
            # so we resort to making a copy of the frozendict
            return dict(obj)
    raise TypeError(
        "Object of type %s is not JSON serializable" % obj.__class__.__name__
    )


# Declare these in the module scope, but they get configured in
# set_json_library.
_canonical_encoder = None
_pretty_encoder = None


def set_json_library(json_lib):
    """
    Set the underlying JSON library that canonicaljson uses to json_lib.

    Params:
        json_lib: The module to use for JSON encoding. Must have a
            `JSONEncoder` property.
    """
    global _canonical_encoder
    _canonical_encoder = json_lib.JSONEncoder(
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
        default=_default,
    )

    global _pretty_encoder
    _pretty_encoder = json_lib.JSONEncoder(
        ensure_ascii=False,
        allow_nan=False,
        indent=4,
        sort_keys=True,
        default=_default,
    )


def encode_canonical_json(json_object):
    """Encodes the shortest UTF-8 JSON encoding with dictionary keys
    lexicographically sorted by unicode code point.

    Args:
        json_object (dict): The JSON object to encode.

    Returns:
        bytes encoding the JSON object"""
    s = _canonical_encoder.encode(json_object)
    return s.encode("utf-8")


def iterencode_canonical_json(json_object):
    """Encodes the shortest UTF-8 JSON encoding with dictionary keys
    lexicographically sorted by unicode code point.

    Args:
        json_object (dict): The JSON object to encode.

    Returns:
        generator which yields bytes encoding the JSON object"""
    for chunk in _canonical_encoder.iterencode(json_object):
        yield chunk.encode("utf-8")


def encode_pretty_printed_json(json_object):
    """
    Encodes the JSON object dict as human readable UTF-8 bytes.

    Args:
        json_object (dict): The JSON object to encode.

    Returns:
        bytes encoding the JSON object"""

    return _pretty_encoder.encode(json_object).encode("utf-8")


def iterencode_pretty_printed_json(json_object):
    """Encodes the JSON object dict as human readable UTF-8 bytes.

    Args:
        json_object (dict): The JSON object to encode.

    Returns:
        generator which yields bytes encoding the JSON object"""

    for chunk in _pretty_encoder.iterencode(json_object):
        yield chunk.encode("utf-8")


if platform.python_implementation() == "PyPy":  # pragma: no cover
    # pypy ships with an optimised JSON encoder/decoder that is faster than
    # simplejson's C extension.
    import json
else:  # pragma: no cover
    # using simplejson rather than regular json on CPython for backwards
    # compatibility (simplejson on Python 3.5 handles parsing of bytes while
    # the standard library json does not).
    #
    # Note that it seems performance is on par or better using json from the
    # standard library as of Python 3.7.
    import simplejson as json

# Set the JSON library to the backwards compatible version.
set_json_library(json)
