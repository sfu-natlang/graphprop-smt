#!/usr/bin/python
from __future__ import division
import sys
from collections import defaultdict
from operator import itemgetter
import heapq, math
from datetime import datetime
import cPickle

max_neighbors_threshold=20
#max_neighbors_threshold=0
max_translations=20
#remove_stop_words=False
graph_type='bi'
ext='fr'

def load_feature_inverted_index():
    global invertedDict
    sys.stderr.write('%s: loading inverted index\n'%datetime.now().strftime('%H:%M:%S'))
    invertedDict={}
    f=open('DPInv.%s'%ext)
    for line in f:
        feat, lst=line.split('\t')
        invertedDict[feat]=eval(lst)
        
def load_feature_inverted_index_pickled():
    global invertedDict
    sys.stderr.write('%s: loading inverted index\n'%datetime.now().strftime('%H:%M:%S'))
    invertedDict={}
    f=open('DPInv.%s.pickle'%ext)
    while True:
        try:
            feat, lst=cPickle.load(f)
            invertedDict[feat]=lst
        except EOFError:
            break
        

#def load_DP_norms():
    #global dpNormsDict
    #sys.stderr.write('%s: loading DP Normalizers\n'%datetime.now().strftime('%H:%M:%S'))
    #dpNormsDict={}
    #f=open('DPNorm.out')
    #for line in f:
        #feat, lst=line.split('\t')
        #dpNormsDict[feat]=float(lst)

def load_phrase_table():
    global phrase_table
    sys.stderr.write('%s: loading phrase-table\n'%datetime.now().strftime('%H:%M:%S'))
    phrase_table=defaultdict(list)
    f=open('phrase-table.moses.%s'%ext)
    for line in f:
        src, tgt, probs=line.split(' ||| ', 2)
        phrase_table[src].append((tgt, float(probs.split()[2])))

def load_stop_words():
    global stopwords
    stopwords=set()
    sys.stderr.write('%s: loading stopwords\n'%datetime.now().strftime('%H:%M:%S'))
    f=open('stopwords.%s'%ext)
    for line in f:
        stopwords.add(line.strip())

def load_oovs():
    global oovs
    oovs=set()
    sys.stderr.write('%s: loading oovs\n'%datetime.now().strftime('%H:%M:%S'))
    f=open('oovs.%s'%ext)
    for line in f:
        oovs.add(line.strip())        


def push(queue, word, score, index):
    if word in entry_finder:
        entry=entry_finder.pop(word)
        entry[-1]=False  #REMOVED
        entry=[entry[0]+score, word, index, True]
    else:
        entry=[score, word, index, True]
    entry_finder[word]=entry
    heapq.heappush(queue, entry)

def find_top_neighbors(phr, dp_lst):
    global entry_finder	    
    if max_neighbors_threshold<1: 
        sys.stderr.write('max_neighbors_threshold cannot be used in the approx find_top_neighbors\n')
        sys.exit(5)
    phr_len=len(phr.split())
    dp_dict=dict(dp_lst)
    candidates=[list(invertedDict[context_word]) for context_word,_ in dp_lst]
    frontier=[]
    entry_finder={}
    neighbors=defaultdict(float)
    for i in range(len(candidates)):
        neighbor, score1=candidates[i].pop(0)
        dvd=max(phr_len, len(neighbor.split()))
        push(frontier, neighbor, -score1*dp_lst[i][1]/dvd, i)
    sys.stderr.write('%s -> %d\n'%(phr, sum(len(lst) for lst in candidates)))
    while len(neighbors) < 1000 or max_neighbors_threshold==0: # 0 for no limitation
        if len(frontier)==0: break
        score, neighbor, index, valid=heapq.heappop(frontier)
        #if valid==True and neighbor in phrase_table: 
        if valid==True: 
            neighbors[neighbor]+=score
        if len(candidates[index]) > 0:
            new_neighbor, new_score=candidates[index].pop(0)
            dvd=max(phr_len, len(new_neighbor.split()))
            push(frontier, new_neighbor, -new_score*dp_lst[index][1]/dvd, index)
    if phr in neighbors:
        del neighbors[phr]
    for neighbor in neighbors:
        neighbors[neighbor]*=-1
    return neighbors
   

def create_bipartite_graph_approx(phr, dp_lst):
    if phr not in oovs: return  # only oovs pass
    neighbors=find_top_neighbors(phr, dp_lst)
    neighbor_items=[]
    for word, prob in neighbors.items():
        if word in phrase_table:        # make edges only to labeled ones (ignore unlabeled nodes)
            neighbor_items.append((word, prob))
    neighbor_items.sort(key=itemgetter(1), reverse=True)
    del neighbor_items[int(max_neighbors_threshold):]
    normalizer=sum(p for _,p in neighbor_items)
    for neighbor, prob in neighbor_items:
        #print '%s\t%s\t%f'%(neighbor, phr, prob/normalizer)
        print '%s\t%s\t%f'%(phr, neighbor, prob/normalizer) 


def create_bipartite_graph_beam(phr, dp_lst):
    if phr not in oovs: return  # only oovs pass
    phr_len=len(phr.split())
    neighbors=defaultdict(float)
    max_score=-1; threshold=-1
    count=0
    for cont_word,assoc in dp_lst:
        for neighbor, n_assoc in invertedDict[cont_word]:
            #if neighbor in dpNormsDict:
            neighb_len=len(neighbor.split())
            dvd=max(phr_len, neighb_len)
            score=assoc*n_assoc
            if score > max_score:
                max_score=score
                threshold=max_score*0.02
            elif score < threshold: break
            count+=1
            neighbors[neighbor]+=score/dvd
    if phr in neighbors:
        del neighbors[phr]
    neighbor_items=[]
    for word, prob in neighbors.items():
        if word in phrase_table:        # make edges only to labeled ones (ignore unlabeled nodes)
            neighbor_items.append((word, prob))
    neighbor_items.sort(key=itemgetter(1), reverse=True)
    del neighbor_items[int(max_neighbors_threshold):]
    normalizer=sum(p for _,p in neighbor_items)
    for neighbor, prob in neighbor_items:
        #print '%s\t%s\t%f'%(neighbor, phr, prob/normalizer)
        print '%s\t%s\t%f'%(phr, neighbor, prob/normalizer) 
    all_count=sum(len(invertedDict[cont_word]) for cont_word,_ in dp_lst)
    try:
        sys.stderr.write('%s -> %d/%d=%f\n'%(phr, count, all_count, count/all_count))
    except:
        return

def create_bipartite_graph(phr, dp_lst):
    if phr not in oovs: return  # only oovs pass
    phr_len=len(phr.split())
    neighbors=defaultdict(float)
    for cont_word,assoc in dp_lst:
        for neighbor, n_assoc in invertedDict[cont_word]:
            #if neighbor in dpNormsDict:
            neighb_len=len(neighbor.split())
            dvd=max(phr_len, neighb_len)
            neighbors[neighbor]+=assoc*n_assoc/dvd
    if phr in neighbors:
        del neighbors[phr]
    #for neighbor in neighbors:
        #neighb_len=len(neighbor.split())
        ##dvd=1 if phr_len==neighb_len else max(phr_len, neighb_len)        
        #dvd=max(phr_len, neighb_len)
        #neighbors[neighbor]/=(dpNormsDict[phr]*dpNormsDict[neighbor]*dvd)
    #neighbor_items=neighbors.items()
    neighbor_items=[]
    for word, prob in neighbors.items():
        if word in phrase_table:        # make edges only to labeled ones (ignore unlabeled nodes)
            neighbor_items.append((word, prob))
    neighbor_items.sort(key=itemgetter(1), reverse=True)
    del neighbor_items[int(max_neighbors_threshold):]
    normalizer=sum(p for _,p in neighbor_items)
    for neighbor, prob in neighbor_items:
        #print '%s\t%s\t%f'%(neighbor, phr, prob/normalizer)
        print '%s\t%s\t%f'%(phr, neighbor, prob/normalizer) 


def create_tripartite_graph(phr, dp_lst): 
    if phr in phrase_table: return  # only oovs and unlabeled nodes pass
    phr_len=len(phr.split())
    neighbors=defaultdict(float)
    is_phr_oov=phr in oovs  # otherwise it's unlabeled
    for cont_word,assoc in dp_lst:
        for neighbor, n_assoc in invertedDict[cont_word]:
            neighb_len=len(neighbor.split())
            dvd=max(phr_len, neighb_len)            
            neighbors[neighbor]+=assoc*n_assoc/dvd
    if phr in neighbors:
        del neighbors[phr]
    labeled_items=[]
    unlabeled_items=[]
    neighbor_phrs=neighbors.keys()
    for neighbor in neighbor_phrs: # make edges from O to both L and U and from U only to L
        if neighbor in oovs: # no such edge {U, O} -> O
            del neighbors[neighbor]
            continue
        if not is_phr_oov and neighbor not in phrase_table: # no edge from U to U
            del neighbors[neighbor]
            continue 
        #prob=neighbors[neighbor]/(dpNormsDict[phr]*dpNormsDict[neighbor])
        #neighbors[neighbor]=prob
        if neighbor in phrase_table:     # O -> L and U -> L
            labeled_items.append((neighbor, neighbors[neighbor]))
        else:  # O -> U
            unlabeled_items.append((neighbor, neighbors[neighbor]))
    labeled_items.sort(key=itemgetter(1), reverse=True)
    if max_neighbors_threshold<1 and len(labeled_items)>0:
        for i in range(len(labeled_items)):
            neighbor, score =labeled_items[i]
            if score < max_neighbors_threshold:
                del labeled_items[i:]
                break
    else:
        del labeled_items[int(max_neighbors_threshold):]
    #del labeled_items[20:]
    if len(unlabeled_items) > 0: 
        unlabeled_items.sort(key=itemgetter(1), reverse=True)
        if max_neighbors_threshold<1 and len(unlabeled_items)>0:
            for i in range(len(unlabeled_items)):
                neighbor, score = unlabeled_items[i]
                if score < max_neighbors_threshold:
                    del unlabeled_items[i:]
                    break
        else:
            del unlabeled_items[int(max_neighbors_threshold/3):]
            #del unlabeled_items[20:]
        #del unlabeled_items[10:]
        neighbor_items=labeled_items+unlabeled_items
        neighbor_items.sort(key=itemgetter(1), reverse=True)
    else:
        neighbor_items=labeled_items
    normalizer=sum(p for _,p in neighbor_items)
    #normalizer=1
    for neighbor, prob in neighbor_items:
        #print '%s\t%s\t%f'%(neighbor, phr, prob/normalizer)
        print '%s\t%s\t%f'%(phr, neighbor, prob/normalizer) 


def create_full_graph(phr, dp_lst): 
    neighbors=defaultdict(float)
    phr_len=len(phr.split())
    for cont_word,assoc in dp_lst:
        for neighbor, n_assoc in invertedDict[cont_word]:
            #if neighbor in dpNormsDict:   # if not, there has been some filtering on DPs e.g. freq-based filtering
            neighb_len=len(neighbor.split())
            dvd=max(phr_len, neighb_len)                
            neighbors[neighbor]+=assoc*n_assoc/dvd
    if phr in neighbors:
        del neighbors[phr]
    #for word in neighbors:
        #neighbors[word]/=(dpNormsDict[phr]*dpNormsDict[word])
    #neighbor_items=neighbors.items()
    labeled_items=[]
    unlabeled_items=[]
    for word, prob in neighbors.items():
        if word in phrase_table:
            labeled_items.append((word, prob))
        else:
            unlabeled_items.append((word, prob))
    labeled_items.sort(key=itemgetter(1), reverse=True)
    del labeled_items[int(max_neighbors_threshold/2):]
    unlabeled_items.sort(key=itemgetter(1), reverse=True)
    del unlabeled_items[int(max_neighbors_threshold/2):]    
    neighbor_items=labeled_items+unlabeled_items;
    neighbor_items.sort(key=itemgetter(1), reverse=True)
    normalizer=sum(p for _,p in neighbor_items)
    for neighbor, prob in neighbor_items:
        #print '%s\t%s\t%f'%(neighbor, phr, prob/normalizer)
        print '%s\t%s\t%f'%(phr, neighbor, prob/normalizer) 

def reducer():
    for line in sys.stdin:
    #for line in open('old/DPs.out'):
        phr, dp=line.split('\t')
        #if remove_stop_words and phr in stopwords: continue;
        dp=eval(dp)
        if phr in phrase_table:
            translations=phrase_table[phr]
            translations.sort(key=itemgetter(1), reverse=True)
            for word, prob in translations[:max_translations]:
                print '***%s\t%s\t%f'%(phr, word, prob)
            if graph_type=='bi' or graph_type=='tri':
                continue;
        if graph_type=='bi':
            create_bipartite_graph(phr, dp);
            #create_bipartite_graph_approx(phr, dp);
            #create_bipartite_graph_beam(phr, dp);
        elif graph_type=='tri':
            create_tripartite_graph(phr, dp);
        elif graph_type=='full':
            create_full_graph(phr, dp);
        else:
            sys.stderr.write('Wrong Graph Type: %s'%graph_type)
            sys.exit(5)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        ext=sys.argv[1]    
    if len(sys.argv) > 2:
        max_neighbors_threshold=float(sys.argv[2])
        sys.stderr.write('max_neighbor=%d\n'%max_neighbors_threshold);
    if len(sys.argv) > 3:
        graph_type=sys.argv[3]
        sys.stderr.write('graph_type=%s\n'%graph_type);    
    if len(sys.argv) > 4:
        max_translations=int(sys.argv[4])
        sys.stderr.write('max_translations=%d\n'%max_translations);
    load_feature_inverted_index();
    #load_feature_inverted_index_pickled()
    #load_DP_norms();
    load_phrase_table()
    load_oovs()
    #if remove_stop_words: load_stop_words()
    reducer()
