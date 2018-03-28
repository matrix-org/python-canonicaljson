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

import re

# using simplejson rather than regular json gives approximately a 25%
# performance improvement (as measured on python 2.7.12/simplejson 3.13.2)
import simplejson as json

from frozendict import frozendict
import sys

__version__ = '1.0.0'

if sys.version_info[0] >= 3:
    def unichr(s):
        return u(chr(s))


def _default(obj):
    if type(obj) is frozendict:
        # fishing the protected dict out of the object is a bit nasty,
        # but we don't really want the overhead of copying the dict.
        return obj._dict
    raise TypeError('Object of type %s is not JSON serializable' %
                    obj.__class__.__name__)


# ideally we'd set ensure_ascii=False, but the ensure_ascii codepath is so
# much quicker (assuming c speedups are enabled) that it's actually much
# quicker to let it do that and then substitute back (it's about 3x faster).
#
# (in any case, simplejson's ensure_ascii doesn't get U+2028 and U+2029 right,
# as per https://github.com/simplejson/simplejson/issues/206).
#
_canonical_encoder = json.JSONEncoder(
    ensure_ascii=True,
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

# here's the magic which we'll use to go from the ensure_ascii-encoded
# output, with its `\uNNNN` escapes, to the raw unicode output.
#
# This regexp matches either `\uNNNN` or `\\`. We match '\\' (and leave it
# unchanged) to make sure that the regex doesn't accidentally capture the uNNNN
# in `\\uNNNN`, which is an escaped backslash followed by 'uNNNN'.
_U_ESCAPE = re.compile(r"\\u([0-9a-f]{4})|\\\\")


def _replace(match):
    g = match.group(1)
    if g is None:
        # escaped backslash
        return '\\\\'
    c = int(g, 16)
    return unichr(c)


def _unescape(s):
    return _U_ESCAPE.sub(_replace, s)


def _default(obj):
    if type(obj) is frozendict:
        return dict(obj)
    raise TypeError('Object of type %s is not JSON serializable' %
                    obj.__class__.__name__)


def encode_canonical_json(json_object):
    """Encodes the shortest UTF-8 JSON encoding with dictionary keys
    lexicographically sorted by unicode code point.

    Args:
        json_object (dict): The JSON object to encode.

    Returns:
        bytes encoding the JSON object"""
    s = _canonical_encoder.encode(json_object)
    s = _unescape(s)
    return s.encode("UTF-8")


def encode_pretty_printed_json(json_object):
    """Encodes the JSON object dict as human readable ascii bytes."""

    return _pretty_encoder.encode(json_object).encode("ascii")
