#!/usr/bin/python

from operator import itemgetter
import sys

prev_word = None
prev_count = 0
word = None

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper.py
    word, count = line.split('\t', 1)

    # convert count (currently a string) to int
    try:
        count = int(count)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if prev_word == word:
        prev_count += count
    else:
        if prev_word:
            # write result to STDOUT
            print '%s\t%s' % (prev_word, prev_count)
        prev_count = count
        prev_word = word

# do not forget to output the last word if needed!
if prev_word == word:
    print '%s\t%s' % (prev_word, prev_count)
