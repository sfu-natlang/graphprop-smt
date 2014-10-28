#!/usr/bin/python
import sys
from collections import defaultdict

def mapper():
    table=defaultdict(list)
    for line in sys.stdin:
	print line

if __name__ == "__main__":
    mapper()
  
