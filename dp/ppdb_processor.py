
# input size(l,xl,xxl) type(lexical)
# output phrase_to_id and id_to_phrase object file, basic_graph (junto format)

import sys
import random
import gzip
import pickle
import codecs

input_file = "ppdb-1.0-l-2gram"
output_file = "ppdb-1.0-l-2gram-dp"
dic={}
weight_type="SCORE"
#weight_type="EgivenF"



with open(input_file) as myinput:

#with codecs.open(input_file,encoding='utf-8') as myinput:
    #with codecs.open(output_file,encoding='utf-8',mode="w") as myoutput:
    with open(output_file,"w") as myoutput:
        for line in myinput:
            #print line
            list = line.split(" ||| ")
            source=list[1]
            target=list[2]
            features=list[3]
            if weight_type == "EgivenF":
                indx = features.find("p(e|f)=")
                temp = features[indx+9:].split()[0]
                score = float(temp)
            elif weight_type == "SCORE":
                d = {}
                for item in features.split():
                    ind = item.split("=")[0]
                    val = item.split("=")[1]
                    if ind != "Alignment":
                                #print ind,val
                        d[ind] = float(val)

                score = d["p(e|f)"]+d["p(f|e)"]+d["p(f|e,LHS)"]+d["p(e|f,LHS)"]+ 100*d["RarityPenalty"]+ 0.3*d["p(LHS|e)"]+0.3*d["p(LHS|f)"]
            #print source,'\t',target,'\t',score
            if not source in dic:
                dic[source]=[(target,score)]
            else:
                if not target in [item[0] for item in dic[source]]:
                    #TODO maximum value
                    dic[source].append((target,score))
        for item in dic.keys():
            trans = dic[item]
            myoutput.write(item+'\t'+str(trans)+'\n')



