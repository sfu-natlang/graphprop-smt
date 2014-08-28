from add_label_to_graph import Labeler 
from pruner import Pruner
from ppdb_processor import Processor

import sys

ppdb_size = "l" # xxl xl l 
ppdb_type = "lexical"
domain = "europarl"
max_number_of_labels = 20
unique_name = domain+"_"+ppdb_size+"_"+ppdb_type+"_"
knn=20
graph_type = "bipartite"

if __name__ == "__main__":
    if len(sys.argv) > 3:
        ppdb_size = sys.argv[1]   # size
        ppdb_type = sys.argv[2]   # type
        domain = sys.argv[3]      # domain
        
        unique_name = domain+"_"+ppdb_size+"_"+ppdb_type+"_"

#        my_processor = Processor(ppdb_size=ppdb_size, 
#                                 ppdb_type=ppdb_type,
#                                 graph_output_file=unique_name+"basic_graph", 
#                                 phrase_to_id_file=unique_name+"phrase_to_id.pkl",
#                                 id_to_phrase_file=unique_name+"id_to_phrase.pkl",
#                                 phase_to_id_helper_file=unique_name+"phrase_to_id") 

        print "starting processing "+unique_name
#        my_processor.process()
        print "end of proessing, Graph file is ready"
     
        print "start transfering labels to the graph nodes"
        my_labeler = Labeler ("../domain/"+domain,
                              unique_name+"basic_graph",
                              unique_name,
                              unique_name+"id_to_phrase.pkl",
                              unique_name+"phrase_to_id.pkl",
                              max_number_of_labels)
        my_labeler.add_labels_to_graph(label_type)
        print "Start of pruning graph"
        my_labeler.prune_graph(unique_name+"basic_graph", unique_name+"seeds", "../domain/europarl/oov_list", graph_type, "knn", knn)
        print "End of pruning graph"
        my_labeler.save_to_file()
        print "transfering label done!"
        print "Now it is ready for propagation"

    else:
        print "You need to pass size, type, and domain to this program"
        print "Something like python command.py xl lexical europarl"
