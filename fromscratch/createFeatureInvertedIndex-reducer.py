#!/usr/bin/python
import sys, cPickle, os
from collections import defaultdict
from operator import itemgetter

def reducer():
    prev_word=None
    word=None
    aggreg_list=None
    for line in sys.stdin:
        word, lst=line.split('\t')
        lst=eval(lst)  # list of pairs [(phr1, sc1), (phr2, sc2), ...]
	if word!=prev_word:
	    if prev_word:
		aggreg_list.sort(key=itemgetter(1), reverse=True)
		print '%s\t%s'%(prev_word, aggreg_list)
		#cPickle.dump((prev_word, aggreg_list), dump_file, -1)
	    prev_word=word
	    aggreg_list=lst
	else:
	    aggreg_list.extend(lst)        

    if prev_word==word:
	aggreg_list.sort(key=itemgetter(1), reverse=True)
	print '%s\t%s'%(prev_word, aggreg_list)
	#cPickle.dump((prev_word, aggreg_list), dump_file, -1)
    #dump_file.close()

if __name__ == "__main__":
    reducer()