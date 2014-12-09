import gzip
import sys
import pickle
from multi_label_extractor import Extractor2
class grammarGenerator:

    def get_phrases(self, tokens):
        return self.ngrams(tokens, 1, 7)


    def ngrams(self, tokens, MIN_N, MAX_N):
        result = []
        n_tokens = len(tokens)
        for i in xrange(n_tokens):
            for j in xrange(i+MIN_N, min(n_tokens, i+MAX_N)+1):
                result.append(" ".join(tokens[i:j]))
        return result

    def __init__(self, extractor, grammar_files_path, grammar_output_files_path, text_file, oov_list_file):
        self.extractor = extractor
        self.text_file = text_file
        self.grammar_files_path = grammar_files_path
        self.grammar_output_files_path = grammar_output_files_path
        self.oov_list = []
        with open(oov_list_file) as inp:
            for line in inp:
                self.oov_list.append(line.strip())


    def unseen_phrases(self,GSCFG=True):
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
                phrases = self.get_phrases(sent.split(" ||| ")[0].split())

                #TODO Named Entity Recognizer
                #print sent
                if GSCFG == True:
                    for phrase in phrases:
                        #print phrase
                        if phrase in self.oov_list:
                            #print word
                            if self.extractor.contains(phrase):
                                #print >> sys.stderr, '%s as an oov phrase found in graph'%phrase
                                label_list = self.extractor.get_labels(phrase)
                                for (rule,p) in label_list:
                                    prob = float(p)
                                    srule = "[X] ||| "+phrase + " ||| "+rule.replace('~~~',phrase, 1)+" ||| EgivenFCoherent=0.0 SampleCountF=0.0 CountEF=0.0 MaxLexFgivenE=0.0 MaxLexEgivenF=0.0 IsSingletonF=1.0 IsSingletonFE=0.0 newF=0.0 "+"Seed="+ str(prob)
                                    new_grammar_file.write(srule+"\n")
                                    #print srule + "\n"
                grammar_file.close()
                new_grammar_file.close()
                i += 1


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
                            #print word
                            if self.extractor.contains(word):
                                #print >> sys.stderr, '%s as an oov phrase found in graph'
                                label_list = self.extractor.get_labels(word)
                                for (rule,p) in label_list:
                                    prob = float(p)
                                    srule = rule.replace('~~~',word, 1)+" ||| EgivenFCoherent=1.0 SampleCountF=1.0 CountEF=1.0 MaxLexFgivenE=1.0 MaxLexEgivenF=1.0 IsSingletonF=1.0 IsSingletonFE=1.0 newF=0.0 "+"Seed="+ str(prob)
                                    new_grammar_file.write(srule+"\n")
                                    #print srule + "\n"
                grammar_file.close()
                new_grammar_file.close()
                i += 1
# TODO fast pass , copy files does not contains any oov.
#    def smooth_all(self):


if __name__=="__main__":


    # for oovs use oov_list , for other use phrase file like dev.phrases

    uniq_prefix = "europarl_en-es_m_phrasal"
    MT_prefix = "../domain/europarl/en-es"
    propagation_prefix = "experiments/europarl_en-es_m_phrasal"

#    testExtractor = Extractor()
#    testExtractor.extract(phrase_list_file=MT_prefix+"/dev.phrases", propagation_output=propagation_prefix+"_finalitr2", id_to_phrase_file=propagation_prefix+"_id_to_phrase.pkl",id_to_label_file=propagation_prefix+"_id_to_label.pkl", max_number_of_labels=100)
#      
#    testGrammarGenerator = grammarGenerator(extractor=testExtractor, grammar_files_path=MT_prefix+"/old/dev.grammars", grammar_output_files_path=MT_prefix+"/europarl_en-es_m_phrasal_itr2/dev.grammars", text_file=MT_prefix+"/dev.en-es", oov_list_file=MT_prefix+"/dev.phrases")
#
#    testGrammarGenerator.unseen_phrases(GSCFG =True)
#
#    testExtractor.extract(phrase_list_file=MT_prefix+"/devtest.phrases", propagation_output=propagation_prefix+"_finalitr2", id_to_phrase_file=propagation_prefix+"_id_to_phrase.pkl",id_to_label_file=propagation_prefix+"_id_to_label.pkl", max_number_of_labels=100)
#
#
#    testGrammarGenerator = grammarGenerator(extractor=testExtractor, grammar_files_path=MT_prefix+"/old/devtest.grammars", grammar_output_files_path=MT_prefix+"/europarl_en-es_m_phrasal_itr2/devtest.grammars", text_file=MT_prefix+"/devtest.en-es", oov_list_file=MT_prefix+"/devtest.phrases")
#
#    testGrammarGenerator.unseen_phrases(GSCFG =True)


    ## europarl_en-es_l_phrasal_label_dic.pkl , europarl_en-es_l_phrasal_graph_dic.pkl 

    uniq_prefix = "europarl_en-es_l_phrasal"
    MT_prefix = "../domain/europarl/en-es"
    propagation_prefix = "madll_experiments/"
    itr_number = "2"


    testExtractor = Extractor2()
    testExtractor.extract(phrase_list_file=MT_prefix+"/dev.phrases", propagation_output=propagation_prefix+uniq_prefix+"_itr"+itr_number, id_to_phrase_file=propagation_prefix+uniq_prefix+"_id_to_phrase.pkl",id_to_label_file=propagation_prefix+uniq_prefix+"_id_to_label.pkl", max_number_of_labels=20)
        
    testGrammarGenerator = grammarGenerator(extractor=testExtractor, grammar_files_path=MT_prefix+"/old/dev.grammars", grammar_output_files_path=MT_prefix+"/"+uniq_prefix+"_itr"+itr_number+"_madll"+"/dev.grammars", text_file=MT_prefix+"/dev.en-es", oov_list_file=MT_prefix+"/dev.phrases")
      
    testGrammarGenerator.unseen_phrases(GSCFG =True)




    testExtractor = Extractor2()
    testExtractor.extract(phrase_list_file=MT_prefix+"/devtest.phrases", propagation_output=propagation_prefix+uniq_prefix+"_itr"+itr_number, id_to_phrase_file=propagation_prefix+uniq_prefix+"_id_to_phrase.pkl",id_to_label_file=propagation_prefix+uniq_prefix+"_id_to_label.pkl", max_number_of_labels=20)
        
    testGrammarGenerator = grammarGenerator(extractor=testExtractor, grammar_files_path=MT_prefix+"/old/devtest.grammars", grammar_output_files_path=MT_prefix+"/"+uniq_prefix+"_itr"+itr_number+"_madll"+"/devtest.grammars", text_file=MT_prefix+"/devtest.en-es", oov_list_file=MT_prefix+"/devtest.phrases")
      
    testGrammarGenerator.unseen_phrases(GSCFG =True)
