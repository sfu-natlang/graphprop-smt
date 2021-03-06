from __future__ import division
import sys, re
from collections import defaultdict

#aggreg_type='useForward'
aggreg_type='addIndctr'
#aggreg_type='addForward'

create_phrase_table=True

def load_oov_align_file():
    global aligned_oovs
    sys.stderr.write('loading oov align file\n')
    aligned_oovs=defaultdict(set)
    oovs=set()
    for line in oov_align_file:
        splits=line.split('\t')
        #print splits[0].strip()
        aligned_oovs[splits[0].strip()].add(splits[1].strip())
        oovs.add(splits[0].strip())

def load_oov_file():
    global oovs
    sys.stderr.write('loading oovs\n')
    oovs=set()
    for line in oov_file:
        oovs.add(line.strip())

def load_phrtable():
    global phrase_pairs
    sys.stderr.write('loading phrase-table\n')
    phrase_pairs=defaultdict(list)
    for line in phrasetable_file:
        splits=line.split(' ||| ');
        src=splits[0].strip()
        tgt=splits[1].strip()
        probs=splits[2].split()[:4]
        #phrase_pairs[src].append((tgt, map(lambda x: 2.7182**float(x), probs)))
        phrase_pairs[src].append((tgt, map(float, probs)))

def evaluate(src, lst):
    rr=[]
    gold=aligned_oovs[src]
    for gold_trans in gold:
        i=0
        for trans in lst:
            i+=1
            if gold_trans==trans:
                rr.append(1.0/i)  # Possibly we can aggregate the scores of same translations generated by different paraphrases
    if len(rr)==0:
        mrr=0;
    else:
        mrr=sum(rr)/len(rr)
    cands=set(lst[:20])
    intersection=gold.intersection(cands)
    recall=len(intersection)/len(gold)

#    if mrr > 0 or recall > 0:
#        print '%s \t MRR=%f\t Recall=%f\n'%(src, mrr, recall)
    return mrr, recall

def write_phrasetable(dic):
    # Add non-oov phrases from the baseline phrase-table       
    aggreg_type='addForward'
    for src in phrase_pairs:
        for (tgt, probs) in phrase_pairs[src]:
            dic['%s ||| %s'%(src, tgt)]=probs+[1];
    keys=dic.keys()
    keys.sort()
    for key in keys:
        probs = dic[key];
        if aggreg_type=='useForward':
            if probs[4]==1: # non-oov
                output_file.write('%s ||| %s 2.718 ||| ||| \n'%(key, ' '.join(map(str, probs[:4]))))
            else: # oov
                output_file.write('%s ||| 1.0 1.0 %g 1.0 2.718 ||| ||| \n'%(key, probs[2]))
        elif aggreg_type=='addForward':
            if probs[4]==1: # non-oov
                output_file.write('%s ||| %s 2.718 1.0 ||| ||| \n'%(key, ' '.join(map(str, probs[:4]))))
            else: # oov
                output_file.write('%s ||| 1.0 1.0 1.0 1.0 2.718 %g ||| ||| \n'%(key, probs[2]))


def create_aggregate_phrasetable():
    mrr=recall=0
    dic={}
    count=0
    for line in label_file:
        sps=filter(lambda x: x!='', line.split('\t'))
        word=sps[0]
        if word not in oovs: continue 
        #print sps[1]
        count+=1
        lbls=re.findall('([^\.\d]+ )+(\d+?\.?\d*?E?-?\d+? )+', sps[1]+' ')
        #print lbls
        if len(lbls)<2: continue
        del lbls[0]
        label_list, prob_list=zip(*lbls)
        label_list=[s.strip() for s in label_list]
        prob_list=map(float, prob_list)
        m, r=evaluate(word, label_list)
        mrr+=m; recall+=r;
        for label, prob in zip(label_list, prob_list):
            dic['%s ||| %s'%(word, label)]=[1, 1, prob, 1, prob]
    print "MRR=%f\t\tRecall=%f\t\toovs=%d\n"%(mrr/count, recall/count, count)
    if create_phrase_table: write_phrasetable(dic)
    #write_phrasetable(dic)



if __name__ == "__main__":
    global label_file, oov_file, oov_align_file, output_file
    create_phrase_table = False
    print "USAGE: python %s label_file, oov_file, oov_align_file, phrasetable_file output_file\n"
    label_file=open(sys.argv[1])
    oov_file=open(sys.argv[2])
    oov_align_file=open(sys.argv[3])
    phrasetable_file=open(sys.argv[4])
    if create_phrase_table: 
        output_file=open(sys.argv[5], 'w')
        load_phrtable()
    if len(sys.argv)>6:
        aggreg_type=sys.argv[6]
    load_oov_align_file()
    load_oov_file()
    create_aggregate_phrasetable()

