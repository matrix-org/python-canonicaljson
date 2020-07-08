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
import json

from frozendict import frozendict


__version__ = '1.1.4'


def _default(obj):
    if type(obj) is frozendict:
        # fishing the protected dict out of the object is a bit nasty,
        # but we don't really want the overhead of copying the dict.
        return obj._dict
    raise TypeError('Object of type %s is not JSON serializable' %
                    obj.__class__.__name__)


_canonical_encoder = json.JSONEncoder(
    ensure_ascii=False,
    separators=(',', ':'),
    sort_keys=True,
    default=_default,
)


_pretty_encoder = json.JSONEncoder(
    ensure_ascii=True,
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
    return s.encode("UTF-8")


def encode_pretty_printed_json(json_object):
    """Encodes the JSON object dict as human readable ascii bytes."""

    return _pretty_encoder.encode(json_object).encode("ascii")
