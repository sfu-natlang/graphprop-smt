# this code use extract.ini file to extract SCFGs for each node as a label
#input : extract_path
# Dependency : Cdec

import cdec
import pickle
from pruner import Pruner

class Labeler:

    extract_path = ""
    graph_file = ""
    save_file_name=""
    label_to_id = {}
    id_to_label = {}

    label_counter = 0
    max_number_of_labels = 20
    processed_nodes = []
    labeled_nodes =[]

    def __init__(self, extract_path, graph_file, save_file_name, id_to_phrase_file, phrase_to_id_file ,max_number_of_labels=20):
        self.extract_path = extract_path
        self.graph_file = graph_file
        self.extractor = cdec.sa.GrammarExtractor(extract_path+'/extract.ini')
        with open(id_to_phrase_file, 'rb') as input:
            self.id_to_phrase = pickle.load(input)
        with open(phrase_to_id_file, 'rb') as input:
            self.phrase_to_id = pickle.load(input)
        self.max_number_of_labels = max_number_of_labels
        self.save_file_name = save_file_name
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
            with open(self.save_file_name+"seeds","w") as seeds_file:
                for line in graph:
                    for i in [0,1]:  # for both target and source side
                        node = line.strip().split()[i]
                        if not node in self.processed_nodes:
                            phrase = self.id_to_phrase[node]
                            labels = self.get_labels(phrase)
                            if labels:
                                self.labeled_nodes.append(node)
                                for (label,prob) in labels:
                                # write to seed file
                                    seeds_file.write(node+"\t"+label+"\t"+prob+"\n")
                            self.processed_nodes.append(node)
                            j += 1
                            if j % 1000 == 0 : 
                                print str(j)+ " nodes processed" 

    def prune_graph(self, graph_file_name, seed_file_name, oov_list_file, output_graph_type, neighbour_prunning_method, neighbour_prunning_input):
   #oov_list
        oov_list = []
        with open(oov_list_file) as inp:
            for line in inp:
                if line.strip() in self.phrase_to_id:
                    oov_list.append(self.phrase_to_id[line.strip()])

   # Pruning 
        graph = {}
        with open(graph_file_name) as inp:
            for line in inp:
                parts = line.strip().split()
                node1= parts[0]
                node2= parts[1]
                weight= parts[2]
                if node1 in graph:
                    graph[node1].append((node2,weight))
                else:
                    graph[node1] = [(node2,weight)]
        pruner = Pruner()
        new_graph =  pruner.prune(graph, self.labeled_nodes, oov_list, output_graph_type, neighbour_prunning_method, neighbour_prunning_input)
       

   # reading graph file 
        with open(graph_file_name,'r') as inp:
           #TODO add pruning details to the file
            with open(graph_file_name+".pruned",'w') as inp2:
                for line in inp:
                    parts = line.strip().split()
                    if parts[0] in new_graph and parts[1] in new_graph:
                        inp2.write(line)

   # reading seeds file  
        with open(seed_file_name,'r') as inp:
            #TODO add pruning details to the file
            with open(seed_file_name+".pruned",'w') as inp2:
                for line in inp:
                    parts = line.strip().split()
                    if parts[0] in new_graph:
                        inp2.write(line)       

    def save_to_file(self):
        with open(self.save_file_name+'id_to_label.pkl', 'wb') as output:
            pickle.dump(self.id_to_label, output, pickle.HIGHEST_PROTOCOL)
        with open(self.save_file_name+'label_to_id.pkl', 'wb') as output:
            pickle.dump(self.label_to_id, output, pickle.HIGHEST_PROTOCOL)

# TODO main function

if __name__=="__main__":
    my_labeler = Labeler("extract", "basic_graph",  "unit_test_ppdb_processorid_to_phrase.pkl",20)
    my_labeler.add_labels_to_graph()
    my_labeler.save_to_file()
