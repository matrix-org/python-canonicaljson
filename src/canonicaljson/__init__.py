# Copyright 2014 OpenMarket Ltd
# Copyright 2018 New Vector Ltd
# Copyright 2022 The Matrix.org Foundation C.I.C.
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
import functools
import json
from typing import Callable, Generator, Type, TypeVar


__version__ = "2.0.0"


@functools.singledispatch
def _preprocess_for_serialisation(obj: object) -> object:  # pragma: no cover
    """Transform an `obj` into something the JSON library knows how to encode.

    This is only called for types that the JSON library does not recognise.
    """
    raise TypeError(
        "Object of type %s is not JSON serializable" % obj.__class__.__name__
    )


T = TypeVar("T")


def register_preserialisation_callback(
    data_type: Type[T], callback: Callable[[T], object]
) -> None:
    """
    Register a `callback` to preprocess `data_type` objects unknown to the JSON encoder.

    When canonicaljson encodes an object `x` at runtime that its JSON library does not
    know how to encode, it will
      - select a `callback`,
      - compute `y = callback(x)`, then
      - JSON-encode `y` and return the result.

    The `callback` should return an object that is JSON-serialisable by the stdlib
    json module.

    If this is called multiple times with the same `data_type`, the most recently
    registered callback is used when serialising that `data_type`.
    """
    if data_type is object:
        raise ValueError("Cannot register callback for the `object` type")
    _preprocess_for_serialisation.register(data_type, callback)


# Declare these once for re-use.
_canonical_encoder = json.JSONEncoder(
    ensure_ascii=False,
    allow_nan=False,
    separators=(",", ":"),
    sort_keys=True,
    default=_preprocess_for_serialisation,
)
_pretty_encoder = json.JSONEncoder(
    ensure_ascii=False,
    allow_nan=False,
    indent=4,
    sort_keys=True,
    default=_preprocess_for_serialisation,
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
