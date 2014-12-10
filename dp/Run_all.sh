

####### STANDARD Code
timestamp=`date +%Y_%m_%d`
monotext_filename='europarl_v7-1k.en'
ngram=1
language='fr'
directory='/cs/natlang-user/ramtin/new_graph/graphprop-smt/domain/europarl/fr-en/'
monotext_directory='/cs/natlang-user/ramtin/new_graph/graphprop-smt/domain/europarl/monotext/'
experiments_directory='/cs/natlang-user/ramtin/new_graph/graphprop-smt/dp/experiments'

oov_file='oovs.fr'
graph_type='bi' # tri
max_number_of_neighbours=15
phrase_table_file='phrase-table.moses.fr'

iter_number_for_output='10'

sh countFreq.sh $language $ngram $monotext_directory $experiments_directory $monotext_filename

#TODO stopword considering
sh computeDP.sh $language $ngram $monotext_directory $experiments_directory $montext_filename $monotext_filename.$ngram.$timestamp.$language NOSTOP 0


sh computeDPNorm.sh $directory $experiments_directory $monotext_filename.$ngram.$timestamp.$language


sh computeInvertedIndex.sh $directory $experiments_directory $monotext_filename.$ngram.$timestamp.$language


# TODO clean this
sh constructGraph.sh $directory $experiments_directory $monotext_filename.$ngram.$timestamp.$language $graph_type $max_number_of_neighbours $monotext_filename.$ngram.$timestamp.$language.$timestamp.indx $language $phrase_table_file $oov_file


# Evaluation
sh evaluate.sh $experiments_directory/Graph/$monotext_filename.$ngram.$timestamp.$language.$timestamp.graph'_finalitr'$iter_number_for_output



##### BACK UP of old CODE


timestamp='2014_10_07_15'
filename='europarl_v7-1k.en'



#sh countFreq.sh en 1 ../domain/europarl/monotext/ ../domain/europarl/experiments/ europarl_v7-1k.en

#sh computeDP.sh en 2 /cs/natlang-user/ramtin/new_graph/graphprop-smt/domain/europarl/ /cs/natlang-user/ramtin/new_graph/graphprop-smt/domain/europarl/experiments/ $filename $filename.2.$timestamp.en NOSTOP 0

#sh computeDPNorm.sh /cs/natlang-user/ramtin/new_graph/graphprop-smt/domain/europarl/ /cs/natlang-user/ramtin/new_graph/graphprop-smt/domain/europarl/experiments/ $filename.2.$timestamp.en

#sh computeInvertedIndex.sh /cs/natlang-user/ramtin/new_graph/graphprop-smt/domain/europarl/ /cs/natlang-user/ramtin/new_graph/graphprop-smt/domain/europarl/experiments/ $filename.2.$timestamp.en

#sh constructGraph.sh /cs/natlang-user/ramtin/new_graph/graphprop-smt/domain/europarl/en-es/ /cs/natlang-user/ramtin/new_graph/graphprop-smt/domain/europarl/experiments/ $filename.2.$timestamp.en bi 15 $filename.2.$timestamp.en.$timestamp.indx en temp.en oovs.dev.en

# phrase-table.moses.en 


filename='mono.fr'
directory='ppdbVsdp/baseline'
timestamp='2014_11_19_16'
ngram=1


#filename='mono.fr'
#directory='ppdbVsdp/baseline2'
#timestamp='2014_12_01_19'
#ngram=2

#sh countFreq.sh fr $ngram $directory $directory/'experiments' $filename

#sh computeDP.sh fr $ngram $directory $directory/'experiments' $filename $filename.$ngram.$timestamp.fr NOSTOP 0

#sh computeDPNorm.sh $directory $directory/'experiments' $filename.$ngram.$timestamp.fr

#sh computeInvertedIndex.sh $directory $directory/'experiments' $filename.$ngram.$timestamp.fr

## mono.fr.1.2014_11_19_16.fr.2014_11_19_19.indx

#inverted_file='mono.fr.2.2014_12_01_19.fr.2014_12_01_19.indx'

#sh constructGraph.sh $directory $directory/'experiments' $filename.$ngram.$timestamp.fr tri 15 $inverted_file fr phrase-table.fr oovs.fr

graph_file='mono.fr.2.2014_12_01_19.fr.2014_12_02_10.graph' # tripartite dp bigram

graph_file='mono.fr.1.2014_11_19_16.fr.2014_12_08_17.graph'
sh constructGraph.sh $directory $directory/'experiments' $filename.1.$timestamp.fr tri 15 mono.fr.1.2014_11_19_16.fr.2014_11_19_19.indx fr phrase-table.fr oovs.dev.fr

#sh propagate.sh $directory $directory/'experiments' /Graph/$graph_file




#/cs/natlang-user/ramtin/new_graph/graphprop-smt/dp/ppdbVsdp/ppdb-l/experiments/computeDP

#directory='ppdbVsdp/ppdb-l'
#DP_filename='ppdb-1.0-l-lexical-dp'



#directory='ppdbVsdp/ppdb-l-2gram'
#DP_filename='ppdb-1.0-l-2gram-dp'
# ppdb as DP
#sh computeInvertedIndex.sh $directory $directory/'experiments' $DP_filename

#sh computeInvertedIndex.sh $directory $directory/'experiments' $DP_filename

#sh constructGraph.sh $directory $directory/'experiments' $DP_filename bi 25 temp fr phrase-table.fr oovs.fr

#sh constructGraph.sh $directory $directory/'experiments' $DP_filename tri 25 temp fr phrase-table.fr oovs.fr

# bigram ppdb 
# graph file = ppdb-1.0-l-2gram-dp.2014_12_05_19.graph


#graph_file_name='ppdb-1.0-l-lexical-dp.2014_11_21_16.graph'
#graph_file_name='ppdb-1.0-l-lexical-dp.2014_11_22_14.graph'
#graph_file_name='ppdb-1.0-l-lexical-dp.2014_11_26_13.graph' # bipartite ppdb
#graph_file_name='ppdb-1.0-l-lexical-dp.2014_11_26_13.graph' # tripartite ppdb 
#graph_file_name='ppdb-1.0-l-lexical-dp.2014_11_24_11.graph'
#graph_file_name='ppdb-1.0-l-lexical-dp.2014_11_24_12.graph'
#graph_file_name='ppdb-1.0-l-lexical-dp.2014_11_24_13.graph'

graph_file_name='mono.fr.1.2014_11_19_16.fr.2014_11_26_15.graph' # tripartite dp
directory='ppdbVsdp/baseline'


#graph_file_name='mono.fr.1.2014_11_19_16.fr.2014_11_26_17.graph'


#sh propagate.sh $directory $directory/'experiments' /Graph/$graph_file_name





