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

def load_dict(filename):
    voc = set((l.replace('l·', 'ŀ').strip() for l in open(filename)))
    voc.update(('<s>', '</s>', 'NUMBER', 'GARBAGE'))
    return voc

def filter_files(prefix, dictionary_file):
    voc = load_dict(dictionary_file)
    indexfile = open('%s.filtered.index' % prefix, 'w')
    for i in range(1, 1000):
        filename = '%s.%d-grams' % (prefix, i)
        if not os.path.isfile(filename):
            break
        print 'Processing %s...' % filename
        outfile = open('%s.filtered.%d-grams' % (prefix, i), 'w')
        old_num_words = 0
        num_words = 0
        sum_counts = 0
        for line in (l for l in open(filename) if l.strip()):
            words, count = line.rsplit(None, 1)
            if all((word in voc) for word in words.split()):
                print >>outfile, line.strip()
                num_words += 1
                sum_counts += int(count)
            old_num_words += 1
        print >>indexfile, '%d-grams=%d' % (i, num_words)
        print >>indexfile, '%d-grams-sum=%d' % (i+1, sum_counts)
        print '\tWrote %d out of %d n-grams.' % (num_words, old_num_words)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit, 'Usage: %s <file prefix> [<dict file>]' % sys.argv[0]
    dictionary = sys.argv[2] if len(sys.argv) > 2 else '/usr/share/dict/catala'
    filter_files(sys.argv[1], dictionary)
