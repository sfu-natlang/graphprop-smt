####################################
#Author : Ramtin
# $1 graph output directory
# $2 phrase table output directory
# $3 graph output file
#####################################

if [ $# -lt 7 ]
  then
    echo "No arguments supplied"
    echo "args: graph output directory (input), phrase table directory (output) , graph output file (input), oovs file, oovs gold file, phrase table, merge phrase table path "
    exit 1
fi

input_path=$1    # $output_path/$graph_file'_finalitr10'
graph_file=$2/$3
output_path=$2
oov_file=$4
oov_gold_file=$5
phrase_table=$6
merge_phrase_table=$7

#graph_file=/Graph/mono.fr.1.2014_11_19_16.fr.2014_11_26_15.graph

new_file='temp'
cat $graph_file |  sed 's/\~/ /g' | sed 's/|||//g' | sed 's, /,,g' > $new_file

results=`python extract_labels.py $new_file $input_path/$oov_file $input_path/$oov_gold_file $input_path/$phrase_table 0`

#results=`python extract_labels.py $output_path/label_prop_output.mapped $input_path/oovs.dev.fr $input_path/oovs.gold.dev.fr $input_path/phrase-table.fr $output | tail -n 1`


# TODO clean this part
corpus="europarl"
graph_type="tri"
d="0"
l="fr"
n=20
str="$corpus\t\t$graph_type\t\td=$d\t\tn=$n\t\tl=$l\t\t$results\t\t"
echo -e $str | tee -a results.txt
echo -e $str >> $output_path/result.txt


# Phrase Table Integration

touch $graph_file'phrase-table.merged.fr'
for aggreg_type in useForward addForward; do
#echo "python extract_labels2.py $new_file $input_path/oovs.fr $input_path/oovs.gold.fr $input_path/phrase-table.fr $output_path/phrase-table.merged.fr $aggreg_type"
`python extract_labels2.py $new_file $input_path/$oov_file $input_path/$oov_gold_file $input_path/$phrase_table $graph_file'phrase-table.merged.fr' $aggreg_type`
echo "***On whole oovs***"
done

sed --in-place '/__DUMMY__/d' $graph_file'phrase-table.merged.fr'

rm $new_file
