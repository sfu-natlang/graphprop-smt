import sys

# Author : Ramtin Mehdizadeh Seraj (rmehdiza --->@ sfu --->.  ca)


# useage : python all_upto_ngram_oov_finder.py oov_list monolingual_text max_window_size
# Sample files : oov_list = newstest2010.un.oov ,  monolingual_text = newstest2010.lc-tok.en max_window_size = 6

print sys.argv
print len(sys.argv)
if len(sys.argv)> 2:
    OOV_list = []
    max_window_size = sys.argv[3]
    window_size = 0
    with open(sys.argv[1]) as ina:
        for l in ina:
            OOV_list.append(l.strip().split("\t")[0])
    for window_size in xrange(max_window_size):
        with open(sys.argv[2]) as input:
            for line in input:
                words_list = line.strip().split()
                for i in xrange(len(words_list)-window_size+1):
                    window = words_list[i:i+window_size]
                    not_contain_oov = 1
                    for part in window:
                        if part in OOV_list:
                            not_contain_oov = 0 
                    if not_contain_oov == 0:
                        print " ".join(window)  
                 
                #print " ".join(window)
