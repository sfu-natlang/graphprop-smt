import sys
import random
import gzip
import pickle


remaining = {}

dic_of_rules = {} # label number ==> changed_rules
dic_of_rules_reverse = {}
oov_to_rules = {} # oov (key) ==> list of lable numbers
Lable_number= 0
probability_rule_oov = {} # prob of rule and number
oov_has_rules_set = set()
dic_node_number={}

oov_list = set()

propagated_distributions={}

################### reading Propagation Part

j=0
print "reading Propagation part"
with open('final_result','r') as res:
    for line in res:
        #print line
        if line:
            line = line.replace("\t\t\t","\t")
            line = line.replace("\t\t","\t")
            line = line.replace("__DUMMY__","RULEN-1",10)
            p1 = line.split("\t")
	    node =  p1[0]
	    print node
            j += 1
	    if "RULEN" in p1[1]:
	        labels = p1[1].split("RULEN")
                #print labels
                label_list = [] 
                for label in labels:
                    if label : #print label
                        if label.split(" ")[0] != "-1":
                            label_list.append(("RULEN"+label.split(" ")[0],label.split(" ")[1]))
                        #print label.split(" ")[0]
                        #print label.split(" ")[1]
                        #else: 
                            #print "dummy rejected"
                slist=sorted(label_list,key=lambda x: x[1])
                if len(slist)>20:
		    slist= slist[0:20]
                propagated_distributions[node]=slist

print j
#################### reading remaining files
print "loading part"
with open('../dic_of_rules.pkl', 'rb') as input:
    dic_of_rules=pickle.load(input)

with open('../dic_of_rules_reverse.pkl', 'rb') as input:
    dic_of_rules_reverse = pickle.load(input)

with open('../oov_to_rules.pkl', 'rb') as input:
    oov_to_rules = pickle.load(input)

with open('../dic_node_number.pkl', 'rb') as input:
    dic_node_number = pickle.load(input)


##################### reading training set
#TODO
with open("europarl/newstest2011.un.oov") as inp:
    for line in inp:
        #print line.split()[0]
        oov_list.add(line.split()[0])

with open("europarl/newstest2012.un.oov") as inp:
    for line in inp:
        oov_list.add(line.split()[0])

# Right now : We are doing full graph smoothing

input_file="devtest.en-es"
input_dir=""




# reading rules and files.

with open(input_file) as ll:
    i = 0
    for line in ll:
        EN = line.strip().split(" |||")[0]
        grammar_file = gzip.open("old/devtest.grammars/grammar."+str(i)+".gz")
        new_grammar_file = gzip.open("new/devtest.grammars/grammar."+str(i)+".gz",'w')
        for line in grammar_file:
            parts = line.strip().split(" ||| ")
            rule = parts[0:4]
            alignment = parts[4]
                #srule = " ||| ".join(rule)
                #print rule
                #temp = parts[3]
                #rem = parts[3:]
	    rule = " ||| ".join(rule) + " seed=1.0" + " ||| "+ alignment
	    new_grammar_file.write(rule+"\n")
	    #print rule + "\n"
        for word in EN.split():
            node_id = "~~~~"
            #print word
            if word in oov_list:
                #print "oov found"
                if word in dic_node_number: 
                    print word
                    node_id = dic_node_number[word]
                    print node_id
        
            #print node_id
            if node_id in propagated_distributions:
                # before propagation
                #print node_id
                #for rule in oov_to_rules[word]:
		#    new_rule = dic_of_rules[rule]
                #    prob = 0.7

                # after Propagation
                #node_id = dic_node_number[word] 
		for (rule,p) in propagated_distributions[node_id]:
		    new_rule = dic_of_rules[rule]
                    prob = float(p)
                   
                    srule = new_rule.replace('~~~',word, 1)+" ||| EgivenFCoherent=1.0 SampleCountF=1.0 CountEF=1.0 MaxLexFgivenE=1.0 MaxLexEgivenF=1.0 IsSingletonF=1.0 IsSingletonFE=1.0 NewF=1.0 "+"seed="+ str(prob)
                    new_grammar_file.write(srule+"\n")
                    #print srule + "\n"

        grammar_file.close()
        new_grammar_file.close()
        #print word +"    " + " # ".join(rules_lists)
        #oov_to_rules[word] = rules_lists
        #if i % 1000 == 0:
            #error_file.write(str(i)+"\n")
        #    print i
        i +=1
 
