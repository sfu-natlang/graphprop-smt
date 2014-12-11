####################################
#Author : Ramtin
# $1 input directory
# $2 output directory
# $3 graph file
# $10 number of map (not in use now) TODO
# $11 number of reduce (not in use now) TODO
#####################################

if [ $# -lt 3 ]
  then
    echo "No arguments supplied"
    echo "args: input directory, output directory , graph file "
    exit 1
fi

##### Streaming hadoop library
jar_file=/usr/lib/hadoop-mapreduce/hadoop-streaming.jar

#####  input information
path_hdfs=/user/rmehdiza/Prop/
input_path=$1
output_path=$2
graph_file=$3


number_of_labels=20
#mapper=identity-mapper.py
#reducer=constructGraph-reducer.py


#TODO replacing space and |||


hadoop fs -mkdir $path_hdfs


# Generating files need for propagation

rm -f $output_path/$graph_file.{seed,graph}
cat $output_path/$graph_file| sed 's/ /\~/g'  | awk -F"\t" "/\*\*\*/ {print substr(\$1, 4)\"\t|||\"\$2\"|||\t\"\$3  >> \"$output_path/$graph_file\"\"_seeds\"} ! /\*\*\*/ {print \$0 >> \"$output_path/$graph_file\"\"_basic_graph\"}"


# Propagation on Single Machine 
#sh /cs/natlang-user/ramtin/new_graph/graphprop-smt/propagation/run_junto_single_machine.sh $output_path/$graph_file


# Propagation on Hadoop (Default)
sh /cs/natlang-user/ramtin/new_graph/graphprop-smt/propagation/run_junto.sh $output_path/$graph_file


#if [ ! $? -eq 0 ]; then exit $?; fi




# TODO cleaning labels

#graph_file=/Graph/mono.fr.1.2014_11_19_16.fr.2014_11_26_15.graph

#new_file='temp'
#cat $output_path/$graph_file'_finalitr10' |  sed 's/\~/ /g' | sed 's/|||//g' | sed 's, /,,g' > $new_file

#print "----------------------"
#touch $output_path/new_phrase_table
#results=`python extract_labels.py $new_file $input_path/oovs.fr $input_path/oovs.gold.fr $input_path/phrase-table.fr $output_path/new_phrase_table`

#echo "python extract_labels.py $new_file $input_path/oovs.fr $input_path/oovs.gold.fr $input_path/phrase-table.fr $output_path/new_phrase_table"
#rm $new_file
#results=`python extract_labels.py $output_path/label_prop_output.mapped $input_path/oovs.dev.fr $input_path/oovs.gold.dev.fr $input_path/phrase-table.fr $output | tail -n 1`


#corpus="europarl"
#graph_type="tri"
#d="0"
#l="fr"
#n=20
#str="$corpus\t\t$graph_type\t\td=$d\t\tn=$n\t\tl=$l\t\t$results\t\t"
#echo -e $str | tee -a results.txt
#echo -e $str >> $output_path/result.txt


# Phrase Table Integration

#for aggreg_type in useForward addForward; do
#echo "python extract_labels2.py $new_file $input_path/oovs.fr $input_path/oovs.gold.fr $input_path/phrase-table.fr $output_path/phrase-table.merged.fr $aggreg_type"
#`python extract_labels2.py $new_file $input_path/oovs.fr $input_path/oovs.gold.fr $input_path/phrase-table.fr $output_path/phrase-table.merged.fr $aggreg_type`
#echo "***On whole oovs***"
#done



