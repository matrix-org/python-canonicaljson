#!/usr/bin/env python
#
# quick benchmark script which loads a bunch of data from an input file, then
# times how long it takes to serialise it

from __future__ import print_function
import json as json
import sys
import timeit

from frozendict import frozendict

import canonicaljson

# try to measure cpu usage time rather than wallclock time, if possible.
try:
    import resource
    RUSAGE_THREAD = 1

    # If the system doesn't support RUSAGE_THREAD then this should throw an
    # exception.
    resource.getrusage(RUSAGE_THREAD)

    def timer():
        r = resource.getrusage(RUSAGE_THREAD)
        return r.ru_utime + r.ru_stime

except Exception:
    timer = timeit.default_timer


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        small_objs = [frozendict(json.loads(line)) for line in f]

    def serialize():
        for o in small_objs:
            canonicaljson.encode_canonical_json(o)

    time = timeit.timeit(serialize, number=10, timer=timer)

    print("%f seconds" % time)
