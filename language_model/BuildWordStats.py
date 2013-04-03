#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright © 2013 Siegfried-A. Gevatter <siegfried@gevatter.com>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import sys
import collections

MIN_COUNT = 5
MAX_N_GRAM = 3

def build_lm(infilename, outfile_prefix):
    infile = open(infilename, 'r')

    counters = []
    for i in range(MAX_N_GRAM):
        counters.append(collections.defaultdict(lambda: 0))

    for lineno, line in enumerate(infile):
        words = ['<s>'] + line.strip().split() + ['</s>']
        accum = collections.deque(maxlen=MAX_N_GRAM)
        for word in words:
            accum.append(word)
            prevs = tuple(accum)
            for i in range(min(len(prevs), MAX_N_GRAM)):
                key = ' '.join(prevs[-i-1:])
                counters[i][key] += 1
        if lineno % 10000 == 0:
            print "Processed %d lines." % lineno
    print "Finished processing %d lines." % lineno

    print "Dumping output..."
    totals = []
    for i in range(MAX_N_GRAM):
        counts = counters[i]
        outfile = open('%s.%d-grams' % (outfile_prefix, i+1), 'w')
        total = 0
        for key, value in counts.iteritems():
            if value >= MIN_COUNT:
                print >>outfile, "%s %d" % (key, value)
                total += value
        totals.append(total)

    outfile = open('%s.index' % outfile_prefix, 'w')
    for i, value in enumerate(totals):
        print >>outfile, "%d-grams=%d" % (i+1, len(counters[i]))
        print >>outfile, "%d-grams-sum=%d" % (i+1, totals[i])

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit, 'Usage: %s <input file> <output prefix>' % sys.argv[0]
    build_lm(sys.argv[1], sys.argv[2])
