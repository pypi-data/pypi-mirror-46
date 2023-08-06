#!/usr/bin/env python
# encoding: utf-8
"""
binpack.py

Created by Maximillian Dornseif on 2010-08-16.
Copyright (c) 2010 HUDORA. All rights reserved.
"""

import time
from pyshipping.package import Package
from pyshipping.package import binpack_simple


def binpack(packages, bin=None, iterlimit=5000):
    return binpack_simple.binpack(packages, bin, iterlimit)


def test(func):
    import time
    from .package import Package
    fd = open('small.txt')
    before = 0
    after = 0
    start = time.time()
    counter = 0
    for line in fd:
        counter += 1
        if counter > 450:
            break
        packages = [Package(pack) for pack in line.strip().split()]
        if not packages:
            continue
        bins, rest = func(packages)
        if rest:
            print(("invalid data", rest, line))
        else:
            before += len(packages)
            after += len(bins)
    # print(time.time() - start)
    print(("Total number of bins required {}".format(after)))


if __name__ == '__main__':
    # print "py",
    test(binpack)



