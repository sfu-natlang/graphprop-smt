
import cdec
import pickle

class GraphConnector:

    extract_path = ""

    lang1_phrase_to_id = {}
    lang2_phrase_to_id = {}

    lang1_id_to_phrase = {}
    lang2_id_to_phrase = {}


    label_to_id = {}
    id_to_label = {}

    label_counter = 0
    max_number_of_labels = 20

    def __init__(self, extract_path, lang1_phrase_to_id_file, lang1_id_to_phrase_file, lang2_phrase_to_id_file, lang2_id_to_phrase_file):

        self.extract_path = extract_path

        self.extractor = cdec.sa.GrammarExtractor(extract_path+'/extract.ini')

        # lang1_phrase_to_id_file lang1_id_to_phrase_file
        with open(lang1_phrase_to_id_file, 'rb') as input:
            self.lang1_phrase_to_id = pickle.load(input)

        with open(lang1_id_to_phrase_file, 'rb') as input:
            self.lang1_id_to_phrase = pickle.load(input)

        # lang2_phrase_to_id_file lang2_id_to_phrase_file
        with open(lang2_phrase_to_id_file, 'rb') as input:
            self.lang2_phrase_to_id = pickle.load(input)

        with open(lang2_id_to_phrase_file, 'rb') as input:
            self.lang2_id_to_phrase = pickle.load(input)
        print "loading done"
# Unk1 = no translation available , Unk2 translation avaiable but not in node list

    def construct(self,graph_connection_file):
        with open(graph_connection_file,'w') as output:
            for key in self.lang1_phrase_to_id.keys():
                grammars = self.extractor.grammar(key)
                for rule in grammars:
                    parts = str(rule).split(" ||| ")
                    source = parts[1]
                    target = parts[2]
                    features = parts[3]
                    loc = features.find("CountEF=")
                    prob = features[loc+8:loc+8+4]

                    translation_found = False
                    node_found = False
                    if source == key:
                        translation_found = True
                        if target in self.lang2_phrase_to_id:
                            node_found = True
                            output.write("%s\t%s\t%s\n"%(self.lang1_phrase_to_id[source],self.lang2_phrase_to_id[target],prob))
                if translation_found == False:
                    output.write("%s\t%s\n"%(self.lang1_phrase_to_id[key],"~~Unk1~~"))
                elif node_found == False:
                    output.write("%s\t%s\n"%(self.lang1_phrase_to_id[key],"~~Unk2~~"))

                       
if __name__=="__main__": 

    prefix = "../graphs/"
    lan1 = "en"
    lan2 = "esp"
    size = "l"
    type = "phrasal"
    domain = "europarl"
    task = "en-es"
    extract_path = "../domain/"+domain+"/"+task
 
    test = GraphConnector(extract_path, prefix+lan1+"_"+size+"_"+type+"_phrase_to_id.pkl",prefix+lan1+"_"+size+"_"+type+"_id_to_phrase.pkl", prefix+lan2+"_"+size+"_"+type+"_phrase_to_id.pkl", prefix+lan1+"_"+size+"_"+type+"_id_to_phrase.pkl")
    
    test.construct(prefix+lan1+"-"+lan2+"-"+size+"-"+type)

