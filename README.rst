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
* Can be configured to encode custom types unknown to the stdlib JSON encoder.

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

A preserialisation hook allows you to encode objects which aren't encodable by the
standard library ``JSONEncoder``.

.. code:: python

    import canonicaljson
    from typing import Dict

    class CustomType:
        pass

    def callback(c: CustomType) -> Dict[str, str]:
        return {"Hello": "world!"}

    canonicaljson.register_preserialisation_callback(CustomType, callback)
    assert canonicaljson.encode_canonical_json(CustomType()) == b'{"Hello":"world!"}'
