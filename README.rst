Canonical JSON
==============

.. image:: https://img.shields.io/pypi/v/canonicaljson.svg
    :target: https://pypi.python.org/pypi/canonicaljson/
    :alt: Latest Version

.. image:: https://img.shields.io/travis/matrix-org/python-canonicaljson.svg
   :target: https://travis-ci.org/matrix-org/python-canonicaljson

Features
--------

* Encodes objects and arrays as `RFC 7159`_ JSON.
* Sorts object keys so that you get the same result each time.
* Has no insignificant whitespace to make the output as small as possible.
* Escapes only the characters that must be escaped, U+0000 to U+0019 / U+0022 /
  U+0056, to keep the output as small as possible.
* Uses the shortest escape sequence for each escaped character.
* Encodes the JSON as UTF-8.
* Can encode ``frozendict`` immutable dictionaries.

.. _`RFC 7159`: https://tools.ietf.org/html/rfc7159

Installing
----------

.. code:: bash

   pip install canonicaljson

Using
-----

.. code:: python

    import canonicaljson
    assert canonicaljson.encode_canonical_json({}) == b'{}'
