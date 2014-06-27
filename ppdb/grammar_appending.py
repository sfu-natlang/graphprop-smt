import gzip
import pickle
from label_extracter import Extractor
class grammarGenerator:
    def __init__(self, extractor, grammar_files_path, grammar_output_files_path, text_file, oov_list_file):
        self.extractor = extractor
        self.text_file = text_file
        self.grammar_files_path = grammar_files_path
        self.grammar_output_files_path = grammar_output_files_path
        self.oov_list = []
        with open(oov_list_file) as inp:
            for line in inp:
                self.oov_list.append(line.strip())
    def just_oovs(self,GSCFG=True):
        with open(self.text_file) as inp:
            i = 0
            for sent in inp:
                grammar_file = gzip.open(self.grammar_files_path+"/grammar."+str(i)+".gz")
                new_grammar_file = gzip.open(self.grammar_output_files_path+"/grammar."+str(i)+".gz",'w')
                for line in grammar_file:
                    parts = line.strip().split(" ||| ")
                    rule = parts[0:4]
                    alignment = parts[4]
                #srule = " ||| ".join(rule)
                #print rule
                #temp = parts[3]
                #rem = parts[3:]
                    rule = " ||| ".join(rule) + " Seed=1.0" + " ||| "+ alignment
                    new_grammar_file.write(rule+"\n")
                    #print rule + "\n"
                # TODO phrase 
                words = sent.split(" ||| ")[0].split()
                
                #TODO Named Entity Recognizer
                print sent
                if GSCFG == True:
                    for word in words:
                        #print word
                        if word in self.oov_list:
                            print word
                            if self.extractor.contains(word):
                                print word
                                label_list = self.extractor.get_labels(word)
                                for (rule,p) in label_list:
                                    prob = float(p)
                                    srule = rule.replace('~~~',word, 1)+" ||| EgivenFCoherent=1.0 SampleCountF=1.0 CountEF=1.0 MaxLexFgivenE=1.0 MaxLexEgivenF=1.0 IsSingletonF=1.0 IsSingletonFE=1.0 "+"Seed="+ str(prob)
                                    new_grammar_file.write(srule+"\n")
                                    print srule + "\n"
                grammar_file.close()
                new_grammar_file.close()
                i += 1
# TODO fast pass , copy files does not contains any oov.
#    def smooth_all(self):


if __name__=="__main__":
    testExtractor = Extractor()
    testExtractor.extract(phrase_list_file="europarl/oov_list", propagation_output="europarl_xl_lexical_iter9_propagation_result", id_to_phrase_file="europarl_xl_lexical_id_to_phrase.pkl",id_to_label_file="id_to_label.pkl", max_number_of_labels=100)
      
    testGrammarGenerator = grammarGenerator(extractor=testExtractor, grammar_files_path="europarl/old/dev.grammars", grammar_output_files_path="europarl/new/dev.grammars", text_file="europarl/dev.en-es", oov_list_file="europarl/oov_list")

    testGrammarGenerator.just_oovs(GSCFG =True)
