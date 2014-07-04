
# input size(l,xl,xxl) type(lexical)
# output phrase_to_id and id_to_phrase object file, basic_graph (junto format)

import sys
import random
import gzip
import pickle


class Processor:
    para_input = "ppdb_files/ppdb-1.0-"+"l"+"-"+"lexical"
    phrase_to_id = {}
    id_to_phrase = {}
    phrase_to_id_file = "phrase_to_id.pkl"
    id_to_phrase_file = "id_to_phrase.pkl"
    phrase_to_id_helper_file = "phrase_to_id"

    graph_output_file="basic_graph"
    
    def __init__(self, ppdb_size="l", ppdb_type="lexical", graph_output_file="basic_graph", \
                 phrase_to_id_file="phrase_to_id.pkl", id_to_phrase_file="id_to_phrase.pkl", phase_to_id_helper_file="phrase_to_id"):
        self.para_input = "ppdb_files"+"/ppdb-1.0-"+ppdb_size+"-"+ppdb_type
        self.phrase_to_id_file = phrase_to_id_file
        self.id_to_phrase_file = id_to_phrase_file
        self.phrase_to_id_helper_file = phase_to_id_helper_file
        self.graph_output_file = graph_output_file
    def process(self):
        i = 0
        print "reading "+self.para_input
        with open(self.para_input) as myinput:
            with open(self.phrase_to_id_helper_file,"w") as file_phrase_to_id:
                with open(self.graph_output_file,"w") as file_basic_graph:
                    for line in myinput:
                        list = line.split(" ||| ")
                        source=list[1]
                        target=list[2]
                        features=list[3]
                        if not source in self.phrase_to_id:
                            self.phrase_to_id[source] = "N"+str(i)
                            self.id_to_phrase["N"+str(i)] = source
                            file_phrase_to_id.write("N"+str(i)+"\t"+source+"\n")
                            i += 1
                        if not target in self.phrase_to_id:
                            self.phrase_to_id[target] = "N"+str(i)
                            self.id_to_phrase["N"+str(i)] = target
                            file_phrase_to_id.write("N"+str(i)+"\t"+target+"\n")
                            i += 1
                        
                        indx = features.find("Lex(e|f)=")
                        #e_given_f = features[indx+9:indx+17]
                        e_given_f = str(float(features[indx+9:indx+12])/100)
                        file_basic_graph.write(self.phrase_to_id[source] + "\t" + self.phrase_to_id[target] + "\t" + e_given_f + "\n")
        print "Total number of nodes: "+str(i)
        print "Saving phrases to files"
        with open(self.phrase_to_id_file, 'wb') as output:
            pickle.dump(self.phrase_to_id, output, pickle.HIGHEST_PROTOCOL)

        with open(self.id_to_phrase_file, 'wb') as output:
            pickle.dump(self.id_to_phrase, output, pickle.HIGHEST_PROTOCOL)

if __name__=="__main__":
   unique_name = "unit_test_ppdb_processor"
   my_processor = Processor(ppdb_size="l", ppdb_type="lexical", graph_output_file=unique_name+"basic_graph", \
                                 phrase_to_id_file=unique_name+"phrase_to_id.pkl", id_to_phrase_file=unique_name+"id_to_phrase.pkl", phase_to_id_helper_file=unique_name+"phrase_to_id") 
   my_processor.process()                                                                              
