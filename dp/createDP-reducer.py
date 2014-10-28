#! /usr/bin/python
from __future__ import division
import sys, math
from operator import itemgetter
from datetime import datetime

context_word_freq_threshold=1  # 0 for no limit
center_phr_freq_threshold=1   # 0 for no limit
dp_max_size=0    # 0 for no limit
association_measure='pmi'
ngram=1
ext='fr'
freq_file_path=''

def readWordFreq():
    global tot_tokens, freqDic, freq_file_path
    tot_tokens=0
    freqDic=dict()
    sys.stderr.write('%s: loading word Frequency file\n'%datetime.now().strftime('%H:%M:%S'))
    freq_file=open(freq_file_path)#open('wordFreq.%dg.%s'%(ngram, ext))
    for line in freq_file:
        splits=line.split('\t')
        freq=int(splits[1])
        freqDic[splits[0]]=freq
        tot_tokens+=freq
        
def load_phrase_table():
    global phrase_table
    sys.stderr.write('%s: loading phrase-table\n'%datetime.now().strftime('%H:%M:%S'))
    phrase_table=set()
    f=open('phrase-table.moses.%s'%ext)
    for line in f:
        src, _=line.split(' ||| ', 1)
        phrase_table.add(src)

def load_oovs():
    global oovs
    oovs=set()
    sys.stderr.write('%s: loading oovs\n'%datetime.now().strftime('%H:%M:%S'))
    f=open('oovs.%s'%ext)
    for line in f:
        oovs.add(line.strip()) 

def assign_association(phr, dp):
    phr_freq=freqDic[phr]
    if center_phr_freq_threshold > 0 and phr_freq <= center_phr_freq_threshold:
        if phr not in oovs: return
        #if phr not in oovs and phr not in phrase_table: return
    if context_word_freq_threshold > 0:
        context_words = dp.keys()   
        for word in context_words:   ## removing context words which are not frequent
            if freqDic[word] <= context_word_freq_threshold:
                del dp[word]
    if association_measure=='cp':
        for word in dp:
            dp[word]=dp[word]/phr_freq
    elif association_measure=='llr':
        negatives=[]
        for word in dp:
            dp[word]=compute_loglikelihood_ratio(dp[word], phr_freq, freqDic[word])
            if dp[word] < 0:
                negatives.append(word)
        for word in negatives:
            del dp[word]
    elif association_measure=='pmi': 
        negatives=[]
        for word in dp:
            dp[word]=math.log((dp[word]*tot_tokens)/(phr_freq*freqDic[word]), 2)
            #dp[word]=math.log(float(dp[word]*no_of_tokens)/(phr_freq*freqDic[word]*coeff), 2)
            if dp[word] < 0:
                negatives.append(word)
        for word in negatives:
            del dp[word]
    elif association_measure=='chi': 
        for word in dp:
            a = dp[word]
            b = phr_freq - a
            c = freqDic[word] - a
            if c == 0: c == 1
            d = tot_tokens - phr_freq - c
            if a+b+c+d != tot_tokens: 
                print "error in chi!"
                exit(1)
            dp[word] = tot_tokens*math.pow(a*d-b*c, 2)/((a+b)*(c+d)*(b+d)*(a+c))
    elif association_measure=='apmi': 
        negatives=[]
        for word in dp:
            a = dp[word]
            b = phr_freq - a
            word_occur = freqDic[word]
            c = word_occur - a
            if c == 0: c ==1
            d = tot_tokens - phr_freq - c
            if a+b+c+d != tot_tokens: 
                print "error in apmi!"
                exit(1)
            dp[word] = a*math.log(a*tot_tokens/(phr_freq*word_occur),2)
            dp[word] += b*math.log(b*tot_tokens/(phr_freq*(tot_tokens-word_occur)),2)
            dp[word] += c*math.log(c*tot_tokens/(word_occur*(tot_tokens-phr_freq)),2)
            dp[word] += d*math.log(d*tot_tokens/((tot_tokens-word_occur)*(tot_tokens-phr_freq)),2)
            dp[word] /=tot_tokens
            if dp[word] < 0:
                negatives.append(word)
        for word in negatives:
            print "negative apmi!!\t", word, dp[word]
            del dp[word] 

    dp_lst=dp.items();
    dp_lst.sort(key=itemgetter(1), reverse=True);
    if dp_max_size > 0 and len(dp_lst)>0:
        if dp_max_size >= 1:
            dp_lst=dp_lst[:int(dp_max_size)]
        else:
            beam_score=dp_lst[0][1]*dp_max_size
            for i in range(len(dp_lst)):
                word, score =dp_lst[i]
                if score < beam_score:
                    del dp_lst[i:]
                    break;
    l2_norm=math.sqrt(sum(map(lambda x: x*x, [val for (_, val) in dp_lst])))
    dp_lst=[(item, int(1000*score/l2_norm)) for item, score in dp_lst]
    print '%s\t%s'%(phr, dp_lst.__str__())
    #print phr, len(dp_lst)

def compute_loglikelihood_ratio(k, n1, n2): # number of coocurrences, frequency of word1, frequency of word2
    def f(k, n):
        p=k/n;
        if p==0 or p==1: 
            return 0
        val= k*math.log(p)+(n-k)*math.log(1-p)
        return val    
    k=min(k, n1, n2)
    return -2*(f(n2, tot_tokens) - f(k, n1) - f(n2 - k, tot_tokens - n1))



def reducer():
    prev_word=None
    word=None
    aggreg_dp=None
    for line in sys.stdin:
    #for line in open('old/intermediate.createDP-mapper.out'):
        word, dp=line.split('\t')
        dp=eval(dp)
        if word!=prev_word:
            if prev_word:
                assign_association(prev_word, aggreg_dp)
            prev_word=word
            aggreg_dp=dp
        else:
            for key, value in dp.items():
                if key in aggreg_dp:
                    aggreg_dp[key]+=value
                else: 
                    aggreg_dp[key]=value
    if prev_word==word:
        assign_association(word, aggreg_dp)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ext=sys.argv[1]    
    if len(sys.argv) > 2:
        dp_max_size=float(sys.argv[2])
        sys.stderr.write('dp_max_size=%f\n'%dp_max_size)
    if len(sys.argv) > 3:
        ngram=int(sys.argv[3])
        sys.stderr.write('ngram=%d\n'%ngram)
    if len(sys.argv) > 4:
        center_phr_freq_threshold=int(sys.argv[4])
        context_word_freq_threshold=int(sys.argv[4])
        sys.stderr.write('center_phr_freq_threshold=%d\n'%center_phr_freq_threshold)
        sys.stderr.write('context_word_freq_threshold=%d\n'%context_word_freq_threshold)
    if len(sys.argv) >5:
        freq_file_path = sys.argv[5]
    readWordFreq()
    if center_phr_freq_threshold>0: 
        load_phrase_table()
        load_oovs()
    reducer()

