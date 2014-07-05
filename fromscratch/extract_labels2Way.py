from __future__ import division
import sys, re
from collections import defaultdict
from operator import itemgetter

#aggreg_type='useForward'
aggreg_type='addIndctr'
#aggreg_type='addForward'

create_phrase_table=True
stopwords=None

#def load_syn_file(filename):
    #global syns, syns_no
    #syns_no=0
    #prev_word=None
    #syns=defaultdict(dict)
    #for line in open(filename):
        #line=line.strip()
        #if line=='': 
            #continue
        #splits=line.split('\t')
        #if len(splits)==1:
            #src_word=splits[0].strip()
            #syns_no+=1
        #elif len(splits)==2:
            #syns[src_word].append((splits[0].strip(), float(splits[1])))
        #elif len(splits)==3:
            #word=splits[0].strip()
            #if word not in aligned_oovs: continue
            #if word != prev_word:
                #syns_no+=1
                #prev_word=word
            #syns[word][splits[1].strip()]=float(splits[2])
        #else:
            #sys.stderr.write('Error!\n')
            #exit()

def load_oov_align_file():
    global aligned_oovs
    sys.stderr.write('loading oov align file\n')
    aligned_oovs=defaultdict(set)
    #oovs=set()
    for line in oov_align_file:
        splits=line.split('\t')
        aligned_oovs[splits[0].strip()].add(splits[1].strip())
        #oovs.add(splits[0].strip())

def load_oov_file():
    global oovs
    sys.stderr.write('loading oovs\n')
    oovs=set()
    for line in oov_file:
        oovs.add(line.strip())

def load_target_stopwords(stopword_filename):
    global stopwords
    stopword_file=open(stopword_filename)
    sys.stderr.write('loading target stopwords\n')
    stopwords=set()
    for line in stopword_file:
        stopwords.add(line.strip())

def load_phrtable():
    global dic
    sys.stderr.write('loading phrase-table\n')
    count=0
    for line in phrasetable_file:
        splits=line.split(' ||| ');
        src=splits[0].strip()
        tgt=splits[1].strip()
        probs=splits[2].split()[:4]
        #phrase_pairs[src].append((tgt, map(lambda x: 2.7182**float(x), probs)))
        #phrase_pairs[src].append((tgt, map(float, probs)))
        dic['%s ||| %s'%(src, tgt)]=map(float, probs)+[1]
        count+=1
        if count%10000==1: print '|',
    print
        

def evaluate(src, lst):
    rr=[]
    
    #lst2=[]
    #prob_lst2=[]
    #for i in range(len(lst)):
        #if lst[i] not in stopwords:
            #lst2.append(lst[i])
            #prob_lst2.append(prob_lst[i]) 
    #lst=lst2[:]
    #prob_lst=prob_lst2[:]
    
    gold=aligned_oovs[src]
    for gold_trans in gold:
        i=0
        for trans in lst:
            i+=1
            if gold_trans==trans:
                rr.append(1.0/i)  # Possibly we can aggregate the scores of same translations generated by different paraphrases
                #print src, trans, i
    if len(rr)==0:
        mrr=0;
    else:
        mrr=sum(rr)/len(rr)
    cands=set(lst[:20])
    intersection=gold.intersection(cands)
    recall=len(intersection)/len(gold)

    #if mrr > 0 or recall > 0:
    #    print '%s \t MRR=%f\t Recall=%f'%(src, mrr, recall)
    return mrr, recall


def write_phrasetable(dic):
    # Add non-oov phrases from the baseline phrase-table       
    #for src in phrase_pairs:
        #for (tgt, probs) in phrase_pairs[src]:
            #dic['%s ||| %s'%(src, tgt)]=probs+[1];
    #load_phrtable()
    keys=dic.keys()
    keys.sort()
    print 'Records to be added to the phrase-table: %d'%len(keys)
    key=keys.pop(0)
    for line in phrasetable_file:
        splits=line.strip().split('|||')
        splits=map(lambda x:x.strip(), splits)
        line_key='%s ||| %s'%(splits[0], splits[1])
        if key==line_key: print key
        while key and key < line_key:
            probs = dic[key];
            src, tgt=key.split(' ||| ')
            write_record(key, probs, ' '.join(['0-%d'%j for j in range(len(tgt.split()))]), '0 0 0')
            if len(keys) > 0:
                key=keys.pop(0)
            else:
                key=None
                break
        if not key or line_key < key:
            line_probs=map(float, splits[2].split())[:-1]+[1]
            write_record(line_key, line_probs, splits[3], splits[4])
            continue
    
def write_record(key, probs, word_align='', counts=''):
    if aggreg_type=='addIndctr':
        entry='%s ||| %s 2.718 %g'%(key, ' '.join(map(str, probs[:4])), probs[4])   
    elif aggreg_type=='useForward':
        if probs[4]==1: # non-oov
            entry='%s ||| %s 2.718'%(key, ' '.join(map(str, probs[:4])))
        else: # oov
            entry='%s ||| %g 1.0 %g 1.0 2.718'%(key, probs[0], probs[2])
    elif aggreg_type=='addForward':
        if probs[4]==1: # non-oov
            entry='%s ||| %s 2.718 1.0 1.0'%(key, ' '.join(map(str, probs[:4])))
        else: # oov
            entry='%s ||| 1.0 1.0 1.0 1.0 2.718 %g %g'%(key, probs[0], probs[2])
    entry=entry+' ||| %s ||| %s\n'%(word_align, counts)
    output_file.write(entry)
    if probs[4]!=1:
        oov_phrtable_file.write(entry)

def parse_label_output_line(str):
    #lbls=re.findall('([^\.\d]+ )+(\d+?\.?\d*?E?-?\d+? )+', sps[1]+' ')
    lbls=re.findall('\|\|\|(.+?)\|\|\| (\d+?\.?\d*?E?-?\d+? )+', str) 
    if len(lbls)==0: return None, None
    #del lbls[0]
    label_list, prob_list=zip(*lbls)
    label_list=[s.strip() for s in label_list]
    prob_list=map(float, prob_list)
    #prob_list=map(lambda x: float(x)**2, prob_list)
    return label_list, prob_list

def ensure_same_word(word, label_list, prob_list):
    pos=0
    if word not in label_list:
        label_list.insert(pos, word)
        prob_list.insert(pos, prob_list[pos]) 
    else:
        i=label_list.index(word)
        word, prob=label_list[i], prob_list[0]
        del label_list[i]
        del prob_list[i]        
        label_list.insert(pos, word)
        prob_list.insert(pos, prob)     

# This method combines the labels from the forward and backward passes and ranks them based on total score
# The weights for p(e|f) and p(f|e) are taken from the baseline system
def create_aggregate_phrasetable_score(w_for, w_rev):
    global dic  # forward and backward weights from 
    
    dic=defaultdict(list)
    mrr=recall=0
    label_file.seek(0); label_file2.seek(0)
    #dic={}
    count=0
    for line in label_file:
        line2=label_file2.readline();
        sps=filter(lambda x: x!='', line.split('\t'))
        word=sps[0]
        if word not in oovs: continue 
        #print sps[1]
        count+=1
        
        label_list_for, prob_list_for = parse_label_output_line(sps[1]+' ')
        if not label_list_for and not prob_list_for: continue
        label_list_rev , prob_list_rev = parse_label_output_line(filter(lambda x: x!='', line2.split('\t'))[1]+' ')
        
        ensure_same_word(word, label_list_for, prob_list_for)
        ensure_same_word(word, label_list_rev, prob_list_rev)
        
        rev_dict=defaultdict(lambda: min(prob_list_rev))
        for_dict=defaultdict(lambda: min(prob_list_for))
        rev_dict.update(dict(zip(label_list_rev, prob_list_rev)))
        for_dict.update(dict(zip(label_list_for, prob_list_for)))
        score_dict={}
        for phr in set(label_list_for+label_list_rev):
            score_dict[phr]=for_dict[phr]**w_for*rev_dict[phr]**w_rev
        score_dict_items=sorted(score_dict.items(), key=itemgetter(1), reverse=True)
        del score_dict_items[20:]
        label_list=[entry for entry, _ in score_dict_items]
        prob_joint=[(for_dict[phr], rev_dict[phr]) for phr in label_list]
        
               
        
        m, r=evaluate(word, label_list)
        #m, r=evaluate(word, lst2, prob_lst2)
        mrr+=m; recall+=r;
        normalizer=sum([x for x,_ in prob_joint])
        normalizer_rev=sum([x for _, x in prob_joint])
        #normalizer=1
        for label, (prob_for, prob_rev) in zip(label_list, prob_joint):
            dic['%s ||| %s'%(word, label)]=[prob_rev/normalizer_rev, 1, prob_for/normalizer, 1, prob_for/normalizer]
            #print '%s ||| %s\t\t %f'%(word, label, prob)
    print "MRR=%f\t\tRecall=%f\t\toovs=%d/%d"%(mrr/len(oovs), recall/len(oovs), count, len(oovs))
    if create_phrase_table: 
        global oov_phrtable_file
        oov_phrtable_file=open(output_file.name+'.oovs', 'w')
        print "creating a file for oovs"
        write_phrasetable(dic)
        oov_phrtable_file.close()

def create_aggregate_phrasetable():
    global dic
    dic=defaultdict(list)
    mrr=recall=0
    #dic={}
    count=0
    for line in label_file:
        line2=label_file2.readline();
        sps=filter(lambda x: x!='', line.split('\t'))
        word=sps[0]
        if word not in oovs: continue 
        #print sps[1]
        count+=1
        
        label_list, prob_list = parse_label_output_line(sps[1]+' ')
        if not label_list and not prob_list: continue
        label_list_rev , prob_list_rev = parse_label_output_line(filter(lambda x: x!='', line2.split('\t'))[1]+' ')
        rev_dict=defaultdict(lambda: min(prob_list_rev))
        rev_dict.update(dict(zip(label_list_rev, prob_list_rev)))
        prob_joint=[(prb, rev_dict[phr]) for phr, prb in zip(label_list, prob_list)]
        
        if stopwords:
            lst2=[]
            prob_lst2=[]
            for i in range(len(label_list)):
                if label_list[i] not in stopwords:
                    lst2.append(label_list[i])
                    prob_lst2.append((prob_list[i], prob_list_rev[i]))
            label_list=lst2[:]
            prob_list=prob_lst2[:]
             
        m, r=evaluate(word, label_list, prob_joint)
        #m, r=evaluate(word, lst2, prob_lst2)
        mrr+=m; recall+=r;
        normalizer=sum([x for x,_ in prob_joint])
        normalizer_rev=sum([x for _, x in prob_joint])
        #normalizer=1
        for label, (prob, prob_rev) in zip(label_list, prob_joint):
            dic['%s ||| %s'%(word, label)]=[prob_rev/normalizer_rev, 1, prob/normalizer, 1, prob/normalizer]
            #print '%s ||| %s\t\t %f'%(word, label, prob)
    print "MRR=%f\t\tRecall=%f\t\toovs=%d/%d"%(mrr/len(oovs), recall/len(oovs), count, len(oovs))
    if create_phrase_table: 
        global oov_phrtable_file
        oov_phrtable_file=open(output_file.name+'.oovs', 'w')
        print "creating a file for oovs"
        write_phrasetable(dic)
        oov_phrtable_file.close()
    

def create_aggregate_phrasetable_dummy():
    mrr=recall=0
    dic={}
    count=0
    for line in label_file:
        sps=filter(lambda x: x!='', line.split('\t'))
        word=sps[0]
        if word not in oovs: continue 
        #print sps[1]
        count+=1
        #lbls=re.findall('([^\.\d]+ )+(\d+?\.?\d*?E?-?\d+? )+', sps[1]+' ')
        lbls=re.findall('\|\|\|(.+?)\|\|\| (\d+?\.?\d*?E?-?\d+? )+', sps[1]+' ')
        if len(lbls)==0: continue
        #del lbls[0]
        label_list, prob_list=zip(*lbls)
        label_list=[s.strip() for s in label_list]
        prob_list=map(float, prob_list)
        if word not in label_list:
            #splits=sps[1].split()
            #dummy_score=splits[splits.index('__DUMMY__')+1]
            #lbls.append((word, float(dummy_score)))
            #lbls=map(lambda x: (x[0].strip(), float(x[1])), lbls)
            #lbls.sort(key=itemgetter(1), reverse=True)
            #label_list, prob_list=zip(*lbls)
            label_list.insert(0, word)
            prob_list.insert(0, prob_list[0])
            #label_list.insert(5, word)
            #prob_list.insert(5, prob_list[5])            
        #else:
        #    prob_list=map(float, prob_list)
            
        #prob_list=map(lambda x: float(x)**2, prob_list)
        m, r=evaluate(word, label_list, prob_list)
        mrr+=m; recall+=r;
        normalizer=sum(prob_list)
        for label, prob in zip(label_list, prob_list):
            dic['%s ||| %s'%(word, label)]=[1, 1, prob/normalizer, 1, prob/normalizer]
    print "MRR=%f\t\tRecall=%f\t\toovs=%d/%d"%(mrr/len(oovs), recall/len(oovs), count, len(oovs))
    #if create_phrase_table: write_phrasetable(dic)



if __name__ == "__main__":
    global label_file, label_file2, oov_file, oov_align_file, output_file
    print "USAGE: python %s label_file, oov_file, oov_align_file, phrasetable_file output_file aggreg_type"%(sys.argv[0])
    label_file=open(sys.argv[1])
    label_file2=open(sys.argv[1]+'2')
    oov_file=open(sys.argv[2])
    try:
        oov_align_file=open(sys.argv[3])
        load_oov_align_file()
    except:
        aligned_oovs={}
    phrasetable_file=open(sys.argv[4])
    if create_phrase_table: 
        output_file=open(sys.argv[5], 'w')
        #load_phrtable()
    if len(sys.argv)>6:
        aggreg_type=sys.argv[6]
        if aggreg_type not in ['useForward', 'addForward', 'addIndctr']:
            create_phrase_table=False
    if len(sys.argv)> 7:
        load_target_stopwords(sys.argv[7])
    
    if aggreg_type=='addIndctr':
        load_syn_file(sys.argv[7])
    load_oov_file()
    #create_aggregate_phrasetable_dummy()
    #label_file.seek(0)
    #create_aggregate_phrasetable()
    
    #w_for=0.034
    #w_rev=0.105
    #w_for=
    w_rev=20
    #for w_for in range(101, 601, 10):
    #    print "%d\t%d\t"%(w_for, w_rev),
    #    create_aggregate_phrasetable_score(w_for/100.0, w_rev/100.0)
    create_aggregate_phrasetable_score(1, 0)

