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
from typing import Any, Generator, Optional, Type

try:
    from typing import Protocol
except ImportError:  # pragma: no cover
    from typing_extensions import Protocol  # type: ignore[misc]

frozendict_type: Optional[Type[Any]]
try:
    from frozendict import frozendict as frozendict_type
except ImportError:
    frozendict_type = None  # pragma: no cover

__version__ = "1.6.2"


def _default(obj: object) -> object:  # pragma: no cover
    if type(obj) is frozendict_type:
        # If frozendict is available and used, cast `obj` into a dict
        return dict(obj)  # type: ignore[call-overload]
    raise TypeError(
        "Object of type %s is not JSON serializable" % obj.__class__.__name__
    )


class Encoder(Protocol):  # pragma: no cover
    def encode(self, data: object) -> str:
        pass

    def iterencode(self, data: object) -> Generator[str, None, None]:
        pass

    def __call__(self, *args: Any, **kwargs: Any) -> "Encoder":
        pass


class JsonLibrary(Protocol):
    JSONEncoder: Encoder


# Declare these in the module scope, but they get configured in
# set_json_library.
_canonical_encoder: Encoder = None  # type: ignore[assignment]
_pretty_encoder: Encoder = None  # type: ignore[assignment]


def set_json_library(json_lib: JsonLibrary) -> None:
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


def encode_canonical_json(data: object) -> bytes:
    """Encodes the given `data` as a UTF-8 canonical JSON bytestring.

    This encoding is the shortest possible. Dictionary keys are
    lexicographically sorted by unicode code point.
    """
    s = _canonical_encoder.encode(data)
    return s.encode("utf-8")


def iterencode_canonical_json(data: object) -> Generator[bytes, None, None]:
    """Iteratively encodes the given `data` as a UTF-8 canonical JSON bytestring.

    This yields one or more bytestrings; concatenating them all together yields the
    full encoding of `data`. Building up the encoding gradually in this way allows us to
    encode large pieces of `data` without blocking other tasks.

    This encoding is the shortest possible. Dictionary keys are
    lexicographically sorted by unicode code point.
    """
    for chunk in _canonical_encoder.iterencode(data):
        yield chunk.encode("utf-8")


def encode_pretty_printed_json(data: object) -> bytes:
    """Encodes the given `data` as a UTF-8 human-readable JSON bytestring."""

    return _pretty_encoder.encode(data).encode("utf-8")


def iterencode_pretty_printed_json(data: object) -> Generator[bytes, None, None]:
    """Iteratively encodes the given `data` as a UTF-8 human-readable JSON bytestring.

    This yields one or more bytestrings; concatenating them all together yields the
    full encoding of `data`. Building up the encoding gradually in this way allows us to
    encode large pieces of `data` without blocking other tasks.
    """
    for chunk in _pretty_encoder.iterencode(data):
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
    import simplejson as json  # type: ignore[no-redef]

# Set the JSON library to the backwards compatible version.
set_json_library(json)
