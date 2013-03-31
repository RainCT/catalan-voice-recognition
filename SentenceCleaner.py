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
import sys

extra_chars = re.compile(r'[",;:\(\)\-—\+«»]')
spaces = re.compile(r'\s\s+')

numbers = re.compile(r'\b[0-9]*\.?[0-9]+([e^]?[0-9]+)?\b')
#roman = re.compile(r'\bm{0,4}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})\b')

apostrophes_pre = re.compile(r"[^ ]+\'\b|\b\'[^ ]+")
apostrophes_left = re.compile(r"([ldmnt]')([aeiouh])")
apostrophes_right = re.compile(r"([aeiou])('[nm]|'ls|'hi)")
apostrophes_bad = re.compile(r"[^ ]+\'[^ ]+")

notcatalan = re.compile(
    ur'[^ ]*[^ A-Zabcdefghijklmnopqrstuvwxyzçàíúèéòóŀ][^ ]*')

def clean_sentence(sentence):
    # Special characters (currencies, etc.)
    sentence = sentence.replace(u'€', u'euros')
    sentence = sentence.replace(u'¢', u'cèntims')
    sentence = sentence.replace(u'$', u'dòlars')
    sentence = sentence.replace(u'£', u'lliures')

    # Non-word characters
    sentence = extra_chars.sub(' ', sentence)
    sentence = spaces.sub(' ', sentence)

    # Numbers
    sentence = numbers.sub('NUMBER', sentence)
    #sentence = roman.sub('ROMAN', sentence) - FIXME: regex matches empty

    # Apostrophes
    sentence = sentence.strip("'")
    sentence = apostrophes_left.sub(r'\1 \2', sentence)
    sentence = apostrophes_right.sub(r'\1 \2', sentence)
    sentence = apostrophes_bad.sub('', sentence)

    # Non-Catalan words
    sentence = sentence.replace(u'l·l', u'ŀl')
    sentence = notcatalan.sub('GARBAGE', sentence)

    return sentence.strip()

def process_file(filename):
    for line in open(filename):
        line = line.decode('utf-8')
        line = clean_sentence(line)
        if line.upper() != line: # is there any word remaining?
            print line.encode('utf-8')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit, 'Usage: %s <filename>' % sys.argv[0]
    process_file(sys.argv[1])
