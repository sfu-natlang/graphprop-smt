#!/usr/bin/python
import sys, math
from operator import itemgetter

def reducer():
    for line in sys.stdin:
        word, lst=line.split('\t')
        lst=eval(lst)  # list of pairs [(phr1, sc1), (phr2, sc2), ...]
	s=math.sqrt(sum(map(lambda x: x*x, [val for (_, val) in lst])))
	print '%s\t%s'%(word, s)	

if __name__ == "__main__":
    reducer()
