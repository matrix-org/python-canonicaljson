Version 1.6.0 released 2022-03-04

* `frozendict` is now an optional dependency; it is no longer required.

Version 1.5.0 released 2021-10-20

* Switch CI from Travis to Github Actions
* Add code to handle frozendict implementations using c-extension
* Add tests for Python 3.10
* Remove outdated Debian packaging code

Version 1.4.0 released 2020-09-03

* Fix producing non-standard JSON for Infinity, -Infinity, and NaN. This could
  cause errors when encoding objects into canonical JSON that previously used to
  work, but were incompatible with JSON implementations in other languages.
* Use UTF-8 to fix ASCII encoding errors when data containing Unicode was
  attempted to be pretty-printed.

Version 1.3.0 released 2020-08-14

* The minimum version of simplejson was bumped to 3.14.0.
* Obsolete workaround for slow encoding of Unicode characters was removed.
* New APIs were added to iteratively encode JSON.

Version 1.2.0 released 2020-07-27

* JSON from the standard library is used automatically on PyPy.
* Support for Python versions which are end-of-lifed was dropped, Python >= 3.5
  is supported and tested in continuous integration.
* An API to configure the underlying JSON library was added (`set_json_library`).

Version 1.1.4 released 2018-05-23

 * Fix error when encoding non-BMP characters on UCS-2 python builds
   (fixes issue #12).

Version 1.1.3 released 2018-04-13

 * Bump depencency on frozendict to >=1.0, to fix conflicts with older
   versions.

Version 1.1.2 released 2018-04-12

 * Fix escaping of control characters U+0000 to U+001F AGAIN, which was STILL
   broken in the previous release

Version 1.1.1 released 2018-04-11

 * Fix escaping of control characters U+0000 to U+001F, which was broken in
   the previous release

Version 1.1.0 released 2018-04-06

 * Significant performance improvements
   ([\#7](https://github.com/matrix-org/python-canonicaljson/pull/7),
   [\#8](https://github.com/matrix-org/python-canonicaljson/pull/8),
   [\#9](https://github.com/matrix-org/python-canonicaljson/pull/9))

Version 1.0.0 released 2015-08-21

 * Initial release
