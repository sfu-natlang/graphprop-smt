import sys

# Author : Ramtin Mehdizadeh Seraj (rmehdiza --->@ sfu --->.  ca)


# useage : python all_upto_ngram_oov_finder.py oov_list monolingual_text max_window_size
# Sample files : oov_list = newstest2010.un.oov ,  monolingual_text = newstest2010.lc-tok.en max_window_size = 6



def oov_finder(monolingual_file, test_set):
    vocabs = []
    oovs = []
    with open(monolingual_file) as input:
        for line in input:
            line = line.split("|||")[0]
            list = line.strip().split(" ")
            for item in list:
                if not item in vocabs:
                    vocabs.append(item)
    print "Done with first part"
    with open(test_set) as input:
        for line in input:
            line = line.split("|||")[0]
            list = line.strip().split(" ")
            for item in list:
                if not item in vocabs:
                    oovs.append(item)
    print "Done with second part"
    return oovs


def oov_checker(oovs, monolingual_file):
    vocabs = []
    found_oovs = []
    with open(monolingual_file) as input:
        for line in input:
            line = line.split("|||")[0]
            list = line.strip().split(" ")
            for item in list:
                if not item in vocabs:
                    vocabs.append(item)
    print "Done with third part"
    for item in oovs:
        if item in vocabs:
            if not item in found_oovs:
                found_oovs.append(item)
    return found_oovs

#if len(sys.argv)> 3:
#    oov(finder

monolingual_file1="/cs/natlang-data/Tasks/MT/Parallel_Corpora/en-es/europarl.v7.lc.tok.norm.en-es" 
test_set="/cs/natlang-user/ramtin/git/NatlangMatrix/europarl/en-es/dev.lc-tok.en-es"
monolingual_file2="/cs/natlang-data/Tasks/MT/Parallel_Corpora/fr-es/europarl.v7.lc.tok.norm.fr-es" 
oovs = oov_finder(monolingual_file1, test_set)
oov_found = oov_checker(oovs,monolingual_file2)

print len(oovs)
print len(oov_found)
#print " ".join(oov_found)


'''
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
'''
