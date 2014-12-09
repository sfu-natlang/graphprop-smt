import sys
from ppdb_processor import Processor


if __name__ == "__main__":
    if len(sys.argv) > 4:
        ppdb_size = sys.argv[1]   # size
        ppdb_type = sys.argv[2]   # type
        ppdb_lang = sys.argv[3]   # language
        domain = sys.argv[4]      # domain

        unique_name = "../graphs/"+ppdb_lang+"_"+ppdb_size+"_"+ppdb_type+"_"

        my_processor = Processor(ppdb_size=ppdb_size,
                                 ppdb_type=ppdb_type,
                                 ppdb_lang=ppdb_lang,
                                 graph_output_file=unique_name+"graph",
                                 phrase_to_id_file=unique_name+"phrase_to_id.pkl",
                                 id_to_phrase_file=unique_name+"id_to_phrase.pkl",
                                 phase_to_id_helper_file=unique_name+"phrase_to_id")

        print "starting processing "+unique_name
        my_processor.process()
        print "end of proessing, Graph file is ready"
