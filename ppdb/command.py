from add_label_to_graph import Labeler 
from pruner import Pruner
from ppdb_processor import Processor

import sys

ppdb_size = "xl" # xxl xl l 
ppdb_type = "lexical"
domain = "europarl"
max_number_of_labels = 20
unique_name = domain+"_"+ppdb_size+"_"+ppdb_type+"_"

if __name__ == "__main__":
    if len(sys.argv) > 3:
        ppdb_size = sys.argv[1]
        ppdb_type = sys.argv[2]   
        domain = sys.argv[3]
        my_processor = Processor(ppdb_size="l", ppdb_type="lexical", graph_output_file=unique_name+"basic_graph", \
                                 phrase_to_id_file=unique_name+"phrase_to_id.pkl", id_to_phrase_file=unique_name+"id_to_phrase.pkl", phase_to_id_helper_file=unique_name+"phrase_to_id") 
        my_processor.process()

        #TODO prunner
        my_labeler = Labeler("extract", unique_name+"basic_graph",  unique_name+"id_to_phrase.pkl", max_number_of_labels)
        my_labeler.add_labels_to_graph()
 
