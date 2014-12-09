
import pickle

class Extractor2:
    phrase_propagated_distributions = {}
#    def __init__(self):
#        
#


### TODO replace ~~~ 
    def extract(self, phrase_list_file, propagation_output, id_to_phrase_file, id_to_label_file, max_number_of_labels=100):
        print "updating list of phrases"
        id_to_phrase = {}
        phrase_set = []
        id_to_label = {}
        with open(id_to_phrase_file, 'rb') as input:
            id_to_phrase = pickle.load(input)

        with open(id_to_label_file, 'rb') as input:
            id_to_label = pickle.load(input)



        print len(id_to_phrase)
        with open(phrase_list_file,'r') as input:
            for line in input:
                phrase_set.append(line.strip())
 
        j=0
        print "reading Propagation part"
	with open(propagation_output,'r') as res:
 	    for line in res:
            #print line
                if line:
                    line = line.replace("\t\t\t","\t")
                    line = line.replace("\t\t","\t")
                    line = line.replace("__DUMMY__","L-1",10)
                    p1 = line.split("\t")
                    node =  p1[0]
                    #print node
                    j += 1
                    if "L" in p1[1]:
                        labels = p1[1].split("L")
                        #print labels
                        label_list = []
                        for label in labels:
                            if label : 
                                #print label
                                if label.split(" ")[0] != "-1":
                                    label_list.append((id_to_label["N"+label.split(" ")[0]],label.split(" ")[1]))
                            #print label.split(" ")[0]
                            #print label.split(" ")[1]
                            #else: 
                                #print "dummy rejected"
                        slist=sorted(label_list,key=lambda x: x[1],reverse = True)
                        if len(slist) > max_number_of_labels:
                            slist= slist[0:20]
                        if id_to_phrase[node] in phrase_set:
                            self.phrase_propagated_distributions[id_to_phrase[node]]=slist         
        print "number of line proccessed "+str(j)
 
    def save_to_file(self, file_name):
        with open(file_name, 'wb') as output:
            pickle.dump(self.self.phrase_propagated_distributions, output, pickle.HIGHEST_PROTOCOL)

    def load_from_file(self, file_name):
        with open(file_name, 'rb') as input:
            self.phrase_propagated_distributions=pickle.load(input)

    def get_labels(self, phrase):
        return self.phrase_propagated_distributions[phrase]
   
    def contains(self, phrase):
        if phrase in self.phrase_propagated_distributions:
            return True
        else:
            return False

if __name__=="__main__":
    testExtractor = Extractor()
    testExtractor.extract(phrase_list_file="temp_list", propagation_output="europarl_xl_lexical_iter9_propagation_result", id_to_phrase_file="europarl_xl_lexical_id_to_phrase.pkl",id_to_label_file="id_to_label.pkl", max_number_of_labels=100)
    list = testExtractor.get_labels("here")
    for item in list:
        print item
