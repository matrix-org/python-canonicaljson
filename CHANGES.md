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
   (https://github.com/matrix-org/python-canonicaljson/pull/7,
   https://github.com/matrix-org/python-canonicaljson/pull/8,
   https://github.com/matrix-org/python-canonicaljson/pull/9)

Version 1.0.0 released 2015-08-21

 * Initial release
