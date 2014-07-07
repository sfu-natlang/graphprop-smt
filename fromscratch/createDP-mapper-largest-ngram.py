#!/usr/bin/python
from __future__ import division
import sys, math, os
from operator import itemgetter
from collections import defaultdict

window_size=4
remove_stop_words=False
ngram=1
ext='fr'
numerized=True
oovs=None;
oov_file=None;

def load_stop_words():
    global stopwords
    stopwords=set()
    sys.stderr.write('loading stopwords\n')
    f=open('stopwords.%s'%ext)
    for line in f:
        stopwords.add(line.strip()) 

def load_oov_words():
    global oovs
    f=open(oov_file)
    oovs=set();
    for line in f:
        oovs.add(line.strip())

def mapper():
    dp_cache=defaultdict(lambda:defaultdict(int))  # key=center_phrase   value=dp    
    #for line in open('monotext.fr'):
    for line in sys.stdin:
        line=line.strip()
        tokens=line.split()
        for i in range(len(tokens)):
            #for j in range(1, ngram+1):
            ng=1 if tokens[i] in oovs else ngram;
            for j in range(ng, ng+1):
                phrase=' '.join(tokens[i:i+j])
                #phrase=tuple(tokens[i:i+j])
                #if remove_stop_words and phrase in stopwords: continue
                if remove_stop_words and all(tok in stopwords for tok in tokens[i:i+j]): continue
                l_context=tokens[max(0, i-window_size):i]
                r_context=tokens[min(i+j, len(tokens)-1): i+j+window_size]
                context=l_context+r_context
                dp=dp_cache[phrase]
                for word in context:
                    if not remove_stop_words or word not in stopwords:
                        dp[word]+=1
                #dp_cache[tokens[i]][0]+=1

    for phrase, dp in dp_cache.iteritems():
        print '%s\t%s'%(phrase, dp.__str__()[26:-1])
        
    
#def mapper():
    #dp_cache=defaultdict(lambda:defaultdict(int))  # key=center_word   value=dp    
    #for line in sys.stdin:
        #line=line.strip()
        #tokens=line.split()
        #for i in range(len(tokens)):
            #if remove_stop_words and tokens[i] in stopwords: continue
            #l_context=tokens[max(0, i-window_size):i]
            #r_context=tokens[min(i+1, len(tokens)-1): min(len(tokens), i+window_size+1)]
            #context=l_context+r_context
            #dp=dp_cache[tokens[i]]
            #for word in context:
                #if not remove_stop_words or word not in stopwords:
                    #dp[word]+=1
            ##dp_cache[tokens[i]][0]+=1

    #for word, dp in dp_cache.iteritems():
        #print '%s\t%s'%(word, dp.__str__()[26:-1])    



if __name__ == "__main__":
    if len(sys.argv) > 1:
        ext=sys.argv[1]
    if len(sys.argv) > 2:
        remove_stop_words=sys.argv[2].lower()=='true'
        sys.stderr.write('remove_stop_words=%s\n'%remove_stop_words)
    if len(sys.argv) > 3:
        ngram=int(sys.argv[3])
        sys.stderr.write('creating DPs for %d-grams'%ngram)
    if len(sys.argv) > 4:
        oov_file=sys.argv[4];
        sys.stderr.write('Loading OOV file: %s\n'%oov_file)
        load_oov_words();
    if remove_stop_words:
        load_stop_words()
    mapper()

