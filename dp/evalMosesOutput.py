from __future__ import division
import sys
from collections import defaultdict
gold=defaultdict(set)
trans_dict=defaultdict(set)
def load_gold_alignments():
    global gold
    for line in open(sys.argv[2]):
        splits=line.strip().split('\t', 1)
        if len(splits)==1: splits.append('')
        gold[splits[0]].add(splits[1])
        
def load_alignments():
    global trans_dict
    for line in open(sys.argv[1]):
        splits=line.strip().split('\t')
        trans_dict[splits[0]].add(splits[1])

def evaluate():
    precision=recall=0
    for oov, trans_lst in trans_dict.items():
        if oov not in gold:
            print '%s not translated'
        gold_lst=gold[oov]
        intersection=set(trans_lst).intersection(set(gold_lst))
        recall+=len(intersection)/len(gold_lst)
        precision+=len(intersection)/len(trans_lst)
    n=len(trans_dict)
    print 'Evaluating %d oov translations'%(n)
    print 'Recall=%f\t\tPrecision=%f'%(recall/n, precision/n)


if __name__=="__main__":
    load_gold_alignments()
    load_alignments()
    evaluate()
        
        