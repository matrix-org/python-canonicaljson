# -*- coding: utf-8 -*-

# Copyright 2014 OpenMarket Ltd
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


import simplejson as json

from frozendict import frozendict

__version__ = '1.0.0'


def encode_canonical_json(json_object):
    """Encodes the shortest UTF-8 JSON encoding with dictionary keys
    lexicographically sorted by unicode code point.

    Args:
        json_object (dict): The JSON object to encode.

    Returns:
        bytes encoding the JSON object"""

    return json.dumps(
        json_object,
        ensure_ascii=False,
        separators=(',', ':'),
        sort_keys=True,
        cls=FrozenEncoder
    ).encode("UTF-8")


def encode_pretty_printed_json(json_object):
    """Encodes the JSON object dict as human readable ascii bytes."""

    return json.dumps(
        json_object,
        ensure_ascii=True,
        indent=4,
        sort_keys=True,
        cls=FrozenEncoder
    ).encode("ascii")


class FrozenEncoder(json.JSONEncoder):
    def default(self, obj):
        if type(obj) is frozendict:
            return dict(obj)
        return json.JSONEncoder.default(self, obj)
