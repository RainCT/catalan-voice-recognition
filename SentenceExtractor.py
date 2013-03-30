#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
import glob

splitter = re.compile(r'[!\?]|\.[^0-9]')
extrachars = re.compile(r'[",;:\(\)\-]')
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
            line = spaces.sub(' ', line)
            elems = filter(None, map(lambda x: x.strip('.'), splitter.split(line)))
            accum.extend(elems)

def parse_folder(path):
    for filename in glob.glob(os.path.join(path, '*/wiki_*')):
        parse_file(filename)

if __name__ == '__main__':
    parse_folder('.')
