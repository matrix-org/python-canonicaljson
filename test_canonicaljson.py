# -*- coding: utf-8 -*-
#
# Copyright 2015 OpenMarket Ltd
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

from canonicaljson import (
    encode_canonical_json,
    encode_pretty_printed_json,
)

from frozendict import frozendict

import unittest


class TestCanonicalJson(unittest.TestCase):

    def test_encode_canonical(self):
        self.assertEquals(encode_canonical_json({}), b'{}')

        # ctrl-chars should be encoded.
        self.assertEquals(
            encode_canonical_json(u"text\u0003\r\n"),
            b'"text\\u0003\\r\\n"',
        )

        # quotes and backslashes should be escaped.
        self.assertEquals(
            encode_canonical_json(r'"\ test'),
            b'"\\"\\\\ test"',
        )

        # non-ascii should come out utf8-encoded.
        self.assertEquals(encode_canonical_json({
                u"la merde amusée": u"💩",
        }), b'{"la merde amus\xc3\xa9e":"\xF0\x9F\x92\xA9"}')

        # so should U+2028 and U+2029
        self.assertEquals(
            encode_canonical_json({u"spaces": u"\u2028 \u2029"}),
            b'{"spaces":"\xe2\x80\xa8 \xe2\x80\xa9"}',
        )

        # but we need to watch out for 'u1234' after backslash, which should
        # get encoded to an escaped backslash, followed by u1234
        self.assertEquals(
            encode_canonical_json(u"\\u1234"),
            b'"\\\\u1234"',
        )

    def test_encode_pretty_printed(self):
        self.assertEquals(encode_pretty_printed_json({}), b'{}')

    def test_frozen_dict(self):
        self.assertEquals(
            encode_canonical_json(frozendict({"a": 1})),
            b'{"a":1}',
        )
        self.assertEquals(
            encode_pretty_printed_json(frozendict({"a": 1})),
            b'{\n    "a": 1\n}')

    def test_unknown_type(self):
        class Unknown(object):
            pass
        unknown_object = Unknown()
        with self.assertRaises(Exception):
            encode_canonical_json(unknown_object)


class TestFloatCanonicalJson(unittest.TestCase):

    def test_serialize_nan_and_infinity_as_null(self):
        self.assertEquals(
            encode_canonical_json(float('nan'), allow_floats=True),
            b'null'
        )
        self.assertEquals(
            encode_canonical_json(float('inf'), allow_floats=True),
            b'null'
        )
        self.assertEquals(
            encode_canonical_json(-float('inf'), allow_floats=True),
            b'null'
        )

    def test_uses_scientific_notation(self):
        samples = [
            (0, b'0'),
            (0.00099, b'0.00099'),
            (0.000011, b'0.000011'),
            (0.0000011, b'0.0000011'),
            (0.000001, b'0.000001'),
            (0.00000099, b'9.9e-7'),
            (0.0000001, b'1e-7'),
            (0.000000930258908, b'9.30258908e-7'),
            (0.00000000000068272, b'6.8272e-13'),
            (10 ** 20, b'100000000000000000000'),
            (10 ** 21, b'1e+21'),
            (10 ** 16 * 1.1, b'11000000000000000'),
            ("frequency at 10.0e+04", b'"frequency at 10.0e+04"'),
        ]
        for number, string in samples:
            self.assertEquals(
                encode_canonical_json(number, allow_floats=True),
                string
            )
