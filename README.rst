Canonical JSON
==============

.. image:: https://img.shields.io/pypi/v/canonicaljson.svg
    :target: https://pypi.python.org/pypi/canonicaljson/
    :alt: Latest Version

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

Supports Python versions 3.7 and newer.

.. _`RFC 7159`: https://tools.ietf.org/html/rfc7159

Installing
----------

.. code:: bash

   pip install canonicaljson

Using
-----

To encode an object into the canonicaljson:

.. code:: python

    import canonicaljson
    assert canonicaljson.encode_canonical_json({}) == b'{}'

There's also an iterator version:

.. code:: python

    import canonicaljson
    assert b''.join(canonicaljson.iterencode_canonical_json({})) == b'{}'

The underlying JSON implementation can be chosen with the following:

.. code:: python

    import json
    import canonicaljson
    canonicaljson.set_json_library(json)

.. note::

    By default canonicaljson uses `simplejson`_ under the hood (except for PyPy,
    which uses the standard library json module).

.. _simplejson: https://simplejson.readthedocs.io/
