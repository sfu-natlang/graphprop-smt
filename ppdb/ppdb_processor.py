
# input size(l,xl,xxl) type(lexical)
# output phrase_to_id and id_to_phrase object file, basic_graph (junto format)

import sys
import random
import gzip
import pickle


class Processor:
    para_input = "ppdb-1.0-"+"l"+"-"+"lexical"
    phrase_to_id = {}
    id_to_phrase = {}
    phrase_to_id_file = "phrase_to_id.pkl"
    id_to_phrase_file = "id_to_phrase.pkl"
    phase_to_id_helper_file = "phrase_to_id"

    def __init__(self, ppdb_size="l", ppdb_type="lexical", graph_output_file="basic_graph", \
                 phrase_to_id_file="phrase_to_id.pkl", id_to_phrase_file="id_to_phrase.pkl", phase_to_id_helper_file="phrase_to_id"):
        self.para_input = "ppdb-1.0-"+ppdb_size+"-"+ppdb_type
        self.phrase_to_id_file = phrase_to_id_file
        self.id_to_phrase_file = id_to_phrase_file
        self.phase_to_id_helper_file = phase_to_id_helper_file

    def process(self):
        i = 0
        with open(para_input) as myinput:
            with open(phrase_to_id_helper_file,"w") as file_phrase_to_id:
                with open(graph_output_file,"w") as file_basic_graph:
                    for line in myinput:
                        list = line.split(" ||| ")
                        source=list[1]
                        target=list[2]
                        features=list[3]
                        if not source in phrase_to_id:
                            phrase_to_id[source] = "N"+str(i)
                            id_to_phrase["N"+str(i)] = source
                            file_phrase_to_id.write("N"+str(i)+"\t"+source)
                            i += 1
                        if not target in phrase_to_id:
                            phrase_to_id[target] = "N"+str(i)
                            id_to_phrase["N"+str(i)] = target
                            file_phrase_to_id.write("N"+str(i)+"\t"+target)
                            i += 1
                        
                        indx = features.find("Lex(e|f)=")
                        #e_given_f = features[indx+9:indx+17]
                        e_given_f = str(float(features[indx+9:indx+12])/100)
                        file_basic_graph.write(phrase_to_id[source] + "\t" + phrase_to_id[target] + "\t" + e_given_f + "\n")

        print "saving part"
        with open(phrase_to_id_file, 'wb') as output:
            pickle.dump(phrase_to_id, output, pickle.HIGHEST_PROTOCOL)

        with open(id_to_phrase_file, 'wb') as output:
            pickle.dump(id_to_phrase, output, pickle.HIGHEST_PROTOCOL)

                                                                                 
