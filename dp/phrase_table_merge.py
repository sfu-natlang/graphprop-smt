
## phrase table of dp and , ppdb(oovs)

dp_phrase_table="experiments/Graph/europarl_v7.fr.1.2014_12_10.fr.2014_12_10.graph_finalitr2phrase-table.merged.fr"
oovs_ppdb_table="experiments-bi-ppdb/Graph/ppdb-1.0-l-lexical-dp.2015_01_08.graph_finalitr1phrase-table.merged.fr.oovs"
output="merged_ppdb_dp_bi"

phrase_table1={}

oovs_in_ppdb={}
temp_list={}
keep_rems = {}
keep_features = {}
### reading dp phrase table
#with open(dp_phrase_table) as inp1:
with open(oovs_ppdb_table) as inp2:
    for line in inp2:
        rule = " ||| ".join(line.split(' ||| ')[:2])
        features = line.split(' ||| ')[2]
        last_feature = features.split()[-1]
        rem = line.split(' ||| ')[-1]
        #print rule,last_feature
        oovs_in_ppdb[rule] = last_feature
        keep_rems[rule] = rem
        keep_features[rule] = features 
        if line.split(' ||| ')[0] in temp_list:
            temp_list[line.split(' ||| ')[0]].append(line.split(' ||| ')[1])
        else:
            temp_list[line.split(' ||| ')[0]]= [line.split(' ||| ')[1]]
   
    
# TODO not in dp but in ppdb 
output_writer = open(output,'w')
key_visited=[]
with open(dp_phrase_table) as inp2:
    last_phrase = "~~START_STATE~~"
    temp_list_added = []
    for line in inp2:
        if last_phrase == "~~START_STATE~~":
            last_phrase = line.split(' ||| ')[0]
        if last_phrase != line.split(' ||| ')[0] and last_phrase in temp_list:
            # transfer remaining from ppdb
            for item in temp_list[last_phrase]:
                if item not in temp_list_added:
                    rule = last_phrase+ " ||| " + item
                    print "just in ppdb"
                    print rule +" ||| "+ keep_features[rule][:-1] + " 0.0 " + oovs_in_ppdb[rule] + " |||  ||| " + str(keep_rems[rule]) 
                    output_writer.write(rule +" ||| "+ keep_features[rule][:-1] + " 0.0 " + oovs_in_ppdb[rule] + " |||  ||| " + str(keep_rems[rule])  )
            temp_list_added = []

        rule = " ||| ".join(line.split(' ||| ')[:2])
        features = line.split(' ||| ')[2]
        last_feature = features.split()[-1]
        rem = line.split(' ||| ')[-1]
        
        if rule in oovs_in_ppdb:
            #print "in both"
            #print rule+" ||| "+ features + " " + oovs_in_ppdb[rule] + " ||| " +  str(rem)
            output_writer.write(rule+" ||| "+ features + " " + oovs_in_ppdb[rule] + " |||  ||| " +  str(rem) )
        else:
            #print "not in ppdb"
            #print rule+" ||| "+ features + " 0.0" + " ||| " + str(rem)
            # TODO if dp feature 1.0 change to 1.0
            if features[-1]  == '1.0': 
                val =  '1.0'
            else:
                val = '0.0'
            output_writer.write(rule+" ||| "+ features + " "+val + " |||  ||| " + str(rem))
        
        temp_list_added.append(line.split(' ||| ')[1])


        last_phrase = line.split(' ||| ')[0]
        key_visited.append(last_phrase)
    if last_phrase in temp_list:
            # transfer remaining from ppdb
        for item in temp_list[last_phrase]:
            if item not in temp_list_added:
                rule = last_phrase+ " ||| " + item
                print "just in ppdb"
                print rule +" ||| "+ keep_features[rule][:-1] + " 0.0 " + oovs_in_ppdb[rule] + " |||  ||| " + str(keep_rems[rule])
                output_writer.write(rule +" ||| "+ keep_features[rule][:-1] + " 0.0 " + oovs_in_ppdb[rule] + " |||  ||| " + str(keep_rems[rule])  )
#remaining in ppdb     
for phrase in temp_list.keys():
    if phrase not in key_visited:
         print "forgoten key"+phrase
         for item in temp_list[phrase]:
            if item not in temp_list_added:
                rule = phrase+ " ||| " + item
                print "just in ppdb"
                print rule +" ||| "+ keep_features[rule][:-1] + " 0.0 " + oovs_in_ppdb[rule] + " |||  ||| " + str(keep_rems[rule])
                output_writer.write(rule +" ||| "+ keep_features[rule][:-1] + " 0.0 " + oovs_in_ppdb[rule] + " |||  ||| " + str(keep_rems[rule])  )


output_writer.close()

  


