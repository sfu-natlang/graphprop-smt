# this code use extract.ini file to extract SCFGs for each node as a label
#input : extract_path
# Dependency : Cdec

import cdec
import pickle

class Labeler:

    extract_path = ""
    graph_file = ""
    label_to_id = {}
    id_to_label = {}

    label_counter = 0
    max_number_of_labels = 20
    processed_nodes = []

    def __init__(self, extract_path, graph_file,  id_to_phrase_file, max_number_of_labels=20):
        self.extract_path = extract_path
        self.graph_file = graph_file
        self.extractor = cdec.sa.GrammarExtractor(extract_path+'/extract.ini')
        with open(id_to_phrase_file, 'rb') as input:
            self.id_to_phrase = pickle.load(input)
        self.max_number_of_labels = max_number_of_labels

    # this will return a list of labels with probability
    def get_labels(self, phrase):
        result_list = []
        grammars = self.extractor.grammar(phrase)        
        for rule in grammars:
            parts = str(rule).split(" ||| ")
            rule = parts[0:3]
            srule = " ||| ".join(rule)
            #print rule
            temp = parts[3]
            rem = parts[3:]

            loc = temp.find("CountEF=")
            prob = temp[loc+8:loc+8+4]
            changed_rule = srule.replace(phrase, '~~~', 1)

            #print "#".join(changed_rule)
            #print changed_rule + " ?? " +  srule
            #print word + " " + srule + " " + prob + " " + changed_rule
            label_id = ""
            if changed_rule in self.label_to_id:
                label_id = self.label_to_id[changed_rule]
                
            else:
                label_id = "RULEN"+str(self.label_counter)
                #print "here" + "RULEN"+str(self.label_number)
                self.id_to_label[label_id] = changed_rule
                self.label_to_id[changed_rule] = label_id
                self.label_counter +=1
            result_list.append((label_id,prob))
                ### sorting result list based on probability (for further cutting)
        result_list = sorted(result_list,key=lambda x: x[1], reverse = True)
        
        # cutting top labels
        if len(result_list) > self.max_number_of_labels:
            result_list =  result_list[0:self.max_number_of_labels]

        return result_list

    def add_labels_to_graph(self):
        j = 0
        with open(self.graph_file,"r") as graph:
            with open("seeds","w") as seeds_file:
                for line in graph:
                    for i in [0,1]:  # for both target and source side
                        node = line.strip().split()[i]
                        if not node in self.processed_nodes:
                            phrase = self.id_to_phrase[node]
                            labels = self.get_labels(phrase)
                            if labels:
                                for (label,prob) in labels:
                                # write to seed file
                                    seeds_file.write(node+"\t"+label+"\t"+prob+"\n")
                            self.processed_nodes.append(node)
                            j += 1
                            if j % 1000 == 0 : 
                                print str(j)+ " nodes processed" 

    def save_to_file(self):
        with open('id_to_label.pkl', 'wb') as output:
            pickle.dump(self.id_to_label, output, pickle.HIGHEST_PROTOCOL)
        with open('label_to_id.pkl', 'wb') as output:
            pickle.dump(self.label_to_id, output, pickle.HIGHEST_PROTOCOL)

# TODO main function

if __name__=="__main__":
    my_labeler = Labeler("extract", "basic_graph",  "unit_test_ppdb_processorid_to_phrase.pkl",20)
    my_labeler.add_labels_to_graph()
    my_labeler.save_to_file()
