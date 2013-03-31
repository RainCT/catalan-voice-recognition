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

apostrophes_left = re.compile(r"([ldmnt]')([aeiouh])")
apostrophes_right = re.compile(r"([aeiou])('[nm]|'ls|'hi)")

def clean_sentence(sentence):
    # Apostrophes
    sentence = re.sub(apostrophes_left, r'\1 \2', sentence)
    sentence = re.sub(apostrophes_right, r'\1 \2', sentence)

    return sentence

def process_file(filename):
    for line in open(filename):
        line = clean_sentence(line)
        print line.strip()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit, 'Usage: %s <filename>' % sys.argv[0]
    process_file(sys.argv[1])
