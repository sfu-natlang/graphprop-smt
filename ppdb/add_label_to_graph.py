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
    max_number_of_labels
    processed_nodes = []

    def __init__(self, extract_path, graph_file,  id_to_phrase_file, max_number_of_labels=20):
        self.extract_path = extract_path
        self.graph_file = graph_file
        self.extractor = cdec.sa.GrammarExtractor(extract_path+'\extract.ini')
        with open(id_to_phrase_file, 'rb') as input:
            self.id_to_phrase = pickle.load(input)
        self.max_number_of_labels = max_number_of_labels

    # this will return a list of labels with probability
    def get_labels(self, phrase):
        result_list = []
        grammars = extractor.grammar(phrase)        
        for rule in grammars:
            parts = rule.split(" ||| ")
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
                label_id = "RULEN"+str(label_counter)
                #print "here" + "RULEN"+str(Lable_number)
                id_to_label[label_id] = changed_rule
                label_to_id[changed_rule] = label_id
                label_counter +=1
            result_list.append((label_id,prob))
                ### sorting result list based on probability (for further cutting)
        result_list = sorted(result_list,key=lambda x: x[1], reverse = True)
        
        # cutting top labels
        if len(result_list) > max_number_of_labels:
            result_list =  result_list[:max_number_of_labels]

        return result_list

    def add_labels_to_graph(self):
        with open(self.graph_file,"w") as graph:
            with open("seeds","w") as seeds_file:
                for line in graph:
                    for i in [0,1]:
                        node = line.strip().split()[i]
                        if not node in processed_nodes:
                            phrase = id_to_phrase(node)
                            labels = get_labels(phrase)
                            if labels:
                                for (label,prob) in labels:
                                # write to seed file
                                    seeds_file.write(node+"\t"+label+"\t"+prob+"\n")
                            processed_nodes.add(node)

    def save_to_file(self):
        with open('id_to_label.pkl', 'wb') as output:
            pickle.dump(dic_of_rules, output, pickle.HIGHEST_PROTOCOL)
 

# TODO main function

if __name__=="__main__":
    my_labeler = Labeler("extract", "basic_graph",  "id_to_phrase.pkl")
    my_labeler.add_labels_to_graph()
