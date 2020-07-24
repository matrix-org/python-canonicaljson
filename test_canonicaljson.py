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
    set_json_library,
)

from frozendict import frozendict

import unittest
from unittest import mock


class TestCanonicalJson(unittest.TestCase):

    def test_encode_canonical(self):
        self.assertEqual(encode_canonical_json({}), b'{}')

        # ctrl-chars should be encoded.
        self.assertEqual(
            encode_canonical_json(u"text\u0003\r\n"),
            b'"text\\u0003\\r\\n"',
        )

        # quotes and backslashes should be escaped.
        self.assertEqual(
            encode_canonical_json(r'"\ test'),
            b'"\\"\\\\ test"',
        )

        # non-ascii should come out utf8-encoded.
        self.assertEqual(encode_canonical_json({
                u"la merde amusée": u"💩",
        }), b'{"la merde amus\xc3\xa9e":"\xF0\x9F\x92\xA9"}')

        # so should U+2028 and U+2029
        self.assertEqual(
            encode_canonical_json({u"spaces": u"\u2028 \u2029"}),
            b'{"spaces":"\xe2\x80\xa8 \xe2\x80\xa9"}',
        )

        # but we need to watch out for 'u1234' after backslash, which should
        # get encoded to an escaped backslash, followed by u1234
        self.assertEqual(
            encode_canonical_json(u"\\u1234"),
            b'"\\\\u1234"',
        )

    def test_encode_pretty_printed(self):
        self.assertEqual(encode_pretty_printed_json({}), b'{}')

    def test_frozen_dict(self):
        self.assertEqual(
            encode_canonical_json(frozendict({"a": 1})),
            b'{"a":1}',
        )
        self.assertEqual(
            encode_pretty_printed_json(frozendict({"a": 1})),
            b'{\n    "a": 1\n}')

    def test_unknown_type(self):
        class Unknown(object):
            pass
        unknown_object = Unknown()
        with self.assertRaises(Exception):
            encode_canonical_json(unknown_object)

    def test_set_json(self):
        """Ensure that changing the underlying JSON implementation works."""
        mock_json = mock.Mock(spec=["JSONEncoder"])
        mock_json.JSONEncoder.return_value.encode.return_value = "sentinel"
        try:
            set_json_library(mock_json)
            self.assertEqual(encode_canonical_json({}), b"sentinel")
        finally:
            # Reset the JSON library to whatever was originally set.
            from canonicaljson import json
            set_json_library(json)
