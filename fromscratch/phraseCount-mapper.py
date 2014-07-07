#!/usr/bin/python

import sys
if len(sys.argv)>1:
    ngram=int(sys.argv[1])
else: ngram=1
# input comes from STDIN (standard input)
for line in sys.stdin:
    line = line.strip()
    words = line.split()
    for l in range(1, ngram+1):
        for i in range(len(words)-l+1):
            print '%s\t%d'%(' '.join(words[i:i+l]), 1)
