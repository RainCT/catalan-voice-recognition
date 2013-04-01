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
import glob
#import mlpy
import numpy
from collections import defaultdict

from mfcc import wavToFeatures
from dtw import DTW

# Load reference vectors
numbers = defaultdict(lambda: [])
for filename in glob.glob('../voice/numbers/*/*.wav'):
    i = int(os.path.basename(filename).split('_')[0])
    numbers[i].append(wavToFeatures(filename))

#x = numpy.concatenate([numpy.concatenate(ns) for ns in numbers.itervalues()])
#y = numpy.concatenate([[i]*sum(len(m) for m in ns) for i, ns in numbers.iteritems()])
#lda = mlpy.LDA()
#lda.learn(x, y)

#for i in numbers:
#    numbers[i] = [lda.transform(m) for m in numbers[i]]

def recognize_file(filename):
    query = wavToFeatures(filename)
#    query = lda.transform(query)

    result = []
    sum_scores = 0
    for number, refs in numbers.iteritems():
        #score = min(DTW(ref, query) for ref in refs)
        score = sum(DTW(ref, query) for ref in refs) / len(refs)
        result.append((score, number))
        sum_scores += score

    result.sort()
    return result + [sum_scores]

def print_result(result):
    print 'Hypotheses:'
    sum_scores = float(result.pop())
    for score, number in result[:5]:
        print '\t- %d (%.2f)' % (number, score/sum_scores)

def test_directory(directory):
    score = 0
    count = 0
    print '\t1st hyp\t\t2nd hyp'
    print '-' * 40
    testset = glob.glob(os.path.join(directory, '*_*.wav'))
    for filename in sorted(testset):
        i = int(os.path.basename(filename).split('_')[0])
        result = recognize_file(filename)
        print '%d.\t%d (%.2f)\t%d (%.2f)' % (i, result[0][1],
            result[0][0]/result[-1], result[1][1], result[1][0]/result[-1])
        if i == result[0][1]:
            score += 1
        count += 1
    print " => %d out of %d" % (score, count)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit, 'Usage: %s <wav file or directory>' % (sys.argv[0])
    if os.path.isdir(sys.argv[1]):
        test_directory(sys.argv[1])
    else:
        print_result(recognize_file(sys.argv[1]))
