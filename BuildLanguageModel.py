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

import os
import sys
import math

DISCOUNT = 0.01

def process_stats(n, data, total_count, prev_counts, outfile, build_prevs=False):
    total_count = float(total_count)
    counts = {} if build_prevs else None
    for key, count in data:
        if n > 1:
            total_count = float(prev_counts[key.rsplit(None, 1)[0]])
        prob = (count - DISCOUNT) / total_count
        log_prob = math.log(prob, math.e)
        backoff_weight = 0.0
        print >>outfile, '%.8f %s %.2f' % (log_prob, key, backoff_weight)
        if counts is not None:
            counts[key] = count
    return counts

def build_lm(prefix, outfile_name):
    # Read index file
    total_entries = {}
    total_counts = {}
    with open('%s.index' % prefix) as indexfile:
        for line in indexfile:
            key, value = line.strip().split('=', 1)
            n, data = key.split('-', 1)
            if data == 'grams':
                total_entries[int(n)] = int(value)
            elif data == 'grams-sum':
                total_counts[int(n)] = int(value)
            else:
                print >>sys.stdout, 'Unknown entry: %s' % key

    # Read count files and generate NIST file
    outfile = open(outfile_name, 'w')
    print >>outfile, '\\data\\'
    for n in sorted(total_counts.keys()):
        print >>outfile, 'ngram %d=%d' % (n, total_entries[n])
    prev_counts = None
    max_n = max(total_counts.keys())
    for n in sorted(total_counts.keys()):
        print >>outfile, '\n\\%d-grams' % n
        filename = '%s.%d-grams' % (prefix, n)
        print 'Processing %s...' % filename
        lines = (l.strip().rsplit(None, 1) for l in open(filename) if l.strip())
        lines = ((key, int(count)) for key, count in lines)
        prev_counts = process_stats(n, lines, total_counts[n],
                                    prev_counts, outfile, n < max_n)
        print '\tFinished processing %d-grams.' % n
    print >>outfile, '\n\\end\\'

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit, 'Usage: %s <file prefix> <output file>' % sys.argv[0]
    build_lm(sys.argv[1], sys.argv[2])
