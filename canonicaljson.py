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
import platform

from frozendict import frozendict

__version__ = '1.2.0'


def _default(obj):
    if type(obj) is frozendict:
        # fishing the protected dict out of the object is a bit nasty,
        # but we don't really want the overhead of copying the dict.
        return obj._dict
    raise TypeError('Object of type %s is not JSON serializable' %
                    obj.__class__.__name__)


# ideally we'd set ensure_ascii=False, but the ensure_ascii codepath is so
# much quicker (assuming c speedups are enabled) that it's actually much
# quicker to let it do that and then substitute back (it's about 2.5x faster).
#
# (in any case, simplejson's ensure_ascii doesn't get U+2028 and U+2029 right,
# as per https://github.com/simplejson/simplejson/issues/206).
#

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
        ensure_ascii=True,
        separators=(',', ':'),
        sort_keys=True,
        default=_default,
    )

    global _pretty_encoder
    _pretty_encoder = json_lib.JSONEncoder(
        ensure_ascii=True,
        indent=4,
        sort_keys=True,
        default=_default,
    )


# This regexp matches either `\uNNNN` or `\\`. We match '\\' (and leave it
# unchanged) to make sure that the regex doesn't accidentally capture the uNNNN
# in `\\uNNNN`, which is an escaped backslash followed by 'uNNNN'.
_U_ESCAPE = re.compile(r"\\u([0-9a-f]{4})|\\\\")


def _unascii(s):
    """Unpack `\\uNNNN` escapes in 's' and encode the result as UTF-8

    This method takes the output of the JSONEncoder and expands any \\uNNNN
    escapes it finds (except for \\u0000 to \\u001F, which are converted to
    \\xNN escapes).

    For performance, it assumes that the input is valid JSON, and performs few
    sanity checks.
    """

    # make the fast path fast: if there are no matches in the string, the
    # whole thing is ascii. We have to turn it into a bytes, which is
    # quickest with encode('utf-8')
    m = _U_ESCAPE.search(s)
    if not m:
        return s.encode('utf-8')

    # appending to a string (or a bytes) is slooow, so we accumulate sections
    # of string result in 'chunks', and join them all together later.
    # (It doesn't seem to make much difference whether we accumulate
    # utf8-encoded bytes, or strings which we utf-8 encode after rejoining)
    #
    chunks = []

    # 'pos' tracks the index in 's' that we have processed into 'chunks' so
    # far.
    pos = 0

    while m:
        start = m.start()
        end = m.end()

        g = m.group(1)

        if g is None:
            # escaped backslash: pass it through along with anything before the
            # match
            chunks.append(s[pos:end])
        else:
            # \uNNNN, but we have to watch out for surrogate pairs.
            #
            # str.encode("utf-8") complains about surrogates, so we have to
            # unpack them.
            c = int(g, 16)

            if c < 0x20:
                # leave as a \uNNNN escape
                chunks.append(s[pos:end])
            else:
                if c & 0xfc00 == 0xd800 and s[end:end + 2] == '\\u':
                    esc2 = s[end + 2:end + 6]
                    c2 = int(esc2, 16)
                    if c2 & 0xfc00 == 0xdc00:
                        c = 0x10000 + (((c - 0xd800) << 10) |
                                       (c2 - 0xdc00))
                        end += 6

                chunks.append(s[pos:start])
                chunks.append(chr(c))

        pos = end
        m = _U_ESCAPE.search(s, pos)

    # pass through anything after the last match
    chunks.append(s[pos:])

    return (''.join(chunks)).encode("utf-8")


def encode_canonical_json(json_object):
    """Encodes the shortest UTF-8 JSON encoding with dictionary keys
    lexicographically sorted by unicode code point.

    Args:
        json_object (dict): The JSON object to encode.

    Returns:
        bytes encoding the JSON object"""
    s = _canonical_encoder.encode(json_object)
    return _unascii(s)


def encode_pretty_printed_json(json_object):
    """Encodes the JSON object dict as human readable ascii bytes."""

    return _pretty_encoder.encode(json_object).encode("ascii")


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
