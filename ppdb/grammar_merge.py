import gzip
import pickle
from label_extracter import Extractor
class grammarMerger:
    
    def __init__(self, grammar_files_path1, grammar_files_path2, grammar_output_files_path):
        self.grammar_files_path1 = grammar_files_path1
        self.grammar_files_path2 = grammar_files_path2
        self.grammar_output_files_path = grammar_output_files_path

    def merge(self):
        # TODO from here
        for i in xrange(3003):
            grammar_file1 = gzip.open(self.grammar_files_path1+"/grammar."+str(i)+".gz")
            grammar_file2 = gzip.open(self.grammar_files_path2+"/grammar."+str(i)+".gz")
            new_grammar_file = gzip.open(self.grammar_output_files_path+"/grammar."+str(i)+".gz",'w')
            for line in grammar_file1:
                new_grammar_file.write(line)
            for line in grammar_file2:
                new_grammar_file.write(line)           
            grammar_file1.close()
            grammar_file2.close()
            new_grammar_file.close()
            
if __name__=="__main__":
    testMerger = grammarMerger("../domain/europarl/en-es/old/devtest.grammars","/cs/natlang-user/ramtin/new_graph/en_es/en_es_parl_baseline/devtest.grammars2","../domain/europarl/en-es/devtest.grammars")
    testMerger.merge()

    testMerger = grammarMerger("../domain/europarl/en-es/old/dev.grammars/","/cs/natlang-user/ramtin/new_graph/en_es/en_es_parl_baseline/dev.grammars2/","../domain/europarl/en-es/dev.grammars")
    testMerger.merge()
    

