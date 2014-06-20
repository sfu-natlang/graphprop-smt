
import sys
import random
import gzip
import pickle

para_input = "ppdb-1.0-l-lexical"

remaining = {}
dic_of_rules = {} # lable number ==> changed_rules
dic_of_rules_reverse = {}
oov_to_rules = {} # oov (key ) ==> list of lable numbers
Lable_number= 0
probability_rule_oov = {} # prob of rule and number
oov_has_rules_set = set()

error_file=open("temp_log",'w')

with open("input_for_graph_2") as ll:
    i = 0
    for line in ll:
        word = line.strip().split(" |||")[0]
        oov_has_rules_set.add(word)
        rules_lists = []
        if not word in oov_to_rules:
            grammar_file = gzip.open("graph3/grammar."+str(i)+".gz")
        #with open("graph3/grammar."+str(i)) as grammar_file:
            for line in grammar_file:
                parts = line.strip().split(" ||| ")
                rule = parts[0:3]
                srule = " ||| ".join(rule)
                #print rule
                temp = parts[3]
                rem = parts[3:]
                
                loc = temp.find("CountEF=")
                #print temp
                prob = temp[loc+8:loc+8+4]
                #print prob
                #print word
                changed_rule = srule.replace(word, '~~~', 1)
                #print "#".join(changed_rule)
                #print changed_rule + " ?? " +  srule
                #print word + " " + srule + " " + prob + " " + changed_rule
                lable = ""
                if changed_rule in dic_of_rules_reverse.keys():
                    lable = dic_of_rules_reverse[changed_rule]
                else:
                    lable = "RULEN"+str(Lable_number)
                    #print "here" + "RULEN"+str(Lable_number)
                    dic_of_rules["RULEN"+str(Lable_number)] = changed_rule
                    dic_of_rules_reverse[changed_rule] = "RULEN"+str(Lable_number)
                    Lable_number +=1 
                rules_lists.append(lable) 
                probability_rule_oov[lable+"|||"+word] = prob 
                #remaining[lable+"|||"+word] = rem  # TODO
            grammar_file.close()
        #print word +"    " + " # ".join(rules_lists)
        oov_to_rules[word] = rules_lists
        if i % 1000 == 0: 
            #error_file.write(str(i)+"\n")
            print i
        i += 1

#TODO writing all to the file 

print "saving part"
with open('dic_of_rules.pkl', 'wb') as output:
    pickle.dump(dic_of_rules, output, pickle.HIGHEST_PROTOCOL)

with open('dic_of_rules_reverse.pkl', 'wb') as output:
    pickle.dump(dic_of_rules_reverse, output, pickle.HIGHEST_PROTOCOL)

with open('oov_to_rules.pkl', 'wb') as output:
    pickle.dump(oov_to_rules, output, pickle.HIGHEST_PROTOCOL)

with open('probability_rule_oov.pkl', 'wb') as output:
    pickle.dump(probability_rule_oov, output, pickle.HIGHEST_PROTOCOL)

with open('oov_has_rules_set.pkl', 'wb') as output:
    pickle.dump(oov_has_rules_set, output, pickle.HIGHEST_PROTOCOL)

dic_node_number = {}
i = 1
with open(para_input) as myinput:
    with open("input_graph",'w') as input_graph:
        with open("seeds",'w') as seeds:
                with open("gold_labels",'w') as gold:
                    for line in myinput:
                        list = line.split(" ||| ")
                        #templable = list[0]
                        source=list[1]
                        target=list[2]
                        features=list[3]
                        if not source in dic_node_number:
                            dic_node_number[source] = "N"+str(i)
                            i += 1
                        if not target in dic_node_number:
                            dic_node_number[target] = "N"+str(i)
                            i += 1
                        indx = features.find("Lex(e|f)=")
                        e_given_f = features[indx+9:indx+17]
                        e_given_f2 = str(float(features[indx+9:indx+12])/100)
                        input_graph.write(dic_node_number[source] + "    " + dic_node_number[target] + "    " + e_given_f2 + "\n")
                       
                        if source in oov_to_rules.keys():
                            #lables = ""
                            for rules in oov_to_rules[source]:
                                prob = probability_rule_oov[rules+"|||"+source]
                                seeds.write(dic_node_number[source] + "    " + rules + "    "+prob + "\n")
                        #else:

                        #if random.random() > 0.8:
                        #    seeds.write(dic_node_number[source] + "    " + templable + "    1.0" + "\n")
                        #else:
                        #    gold.write(dic_node_number[source] + "    " + templable + "    1.0" + "\n")


