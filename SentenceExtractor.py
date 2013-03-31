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

import re
import os
import glob

MIN_WORDS_IN_LINE = 4

splitter = re.compile(r'[!\?]|\.[^0-9]')
extrachars = re.compile(r'[",;:\(\)\-]')
extratags = re.compile(r'<[^>]*>')
spaces = re.compile(r'\s\s+')

def parse_file(filename):
    stream = (line.strip() for line in open(filename) if line.strip())
    accum = None
    for line in stream:
        if line.startswith('<doc '):
            accum = []
        elif line == '</doc>':
            print u'\n'.join(accum).encode('utf-8')
            accum = None
        else:
            assert accum is not None
            line = line.decode('utf-8').lower()
            line = extrachars.sub(' ', line)
            line = extratags.sub(' ', line)
            line = spaces.sub(' ', line)
            elems = filter(None, map(lambda x: x.strip('.'), splitter.split(line)))
            elems = filter(lambda x: len(x.split()) >= MIN_WORDS_IN_LINE, elems)
            accum.extend(elems)

def parse_folder(path):
    for filename in glob.glob(os.path.join(path, '*/wiki_*')):
        parse_file(filename)

if __name__ == '__main__':
    parse_folder('.')
