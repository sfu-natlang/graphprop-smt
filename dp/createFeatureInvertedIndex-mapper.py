#!/usr/bin/python
import sys
from collections import defaultdict

def mapper():
    table=defaultdict(list)
    for line in sys.stdin:
    #for line in open('emea/nostop-d0.3.2g-rmvFreq1/DPs.out.id'):
        phr, dp=line.split('\t', 1)
        dp=eval(dp)  # sorted list of pairs [(w1, sc1), (w2, sc2), ...]
        for word, score in dp:
            table[word].append((phr, score))
    for word in table:
        print '%s\t%s'%(word, table[word])


if __name__ == "__main__":
    mapper()
  