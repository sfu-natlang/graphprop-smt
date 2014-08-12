#####################################
#Author : Ramtin
# $1 language
# $2 ngram
# $3 input directory
# $4 output directory
# $5 monotext file
# $6 Frequency Count File
# $7 Stopword file ("NOSTOP" if you dont want to remove stopwords)
# $8 min frequency
# $9 number of map (not in use now) TODO
# $10 number of reduce (not in use now) TODO
#####################################

if [ $# -lt 8 ]
  then
    echo "No arguments supplied"
    echo "args: language , ngram , input directory , output directory , monotext file , frequency file , stopword file , min freq"
    exit 1
fi

##### Streaming hadoop library
jar_file=/usr/lib/hadoop-mapreduce/hadoop-streaming-2.2.0.2.0.6.0-102.jar

#####  input information
path_hdfs=/user/rmehdiza/computeDP/
language=$1
ngram=$2
input_path=$3
output_path=$4
input_file_name=$5
freq_file_name=$6
stop_word_file=$7
min_freq=$8

#TODO changeble d value
d=0.3            # DP pruning | d=0 for no limit, 0<d<1 : beam pruning, d>1 histogram pruning


if [ $stop_word_file == "NOSTOP" ]; then remove_stop_words="false"; else remove_stop_words="true"; fi

package_str=""
#TODO min frequency
#if [ $min_freq -gt 0 ]; then package_str=" -file phrase-table.moses.$language -file oovs.$language"; else package_str=""; fi
 #hadoop fs -copyFromLocal phrase-table.moses.$lan $path_hdfs
 #hadoop fs -copyFromLocal oov.$lan $path_hdfs
 #hadoop fs -copyFromLocal phrase-table.moses.out $dir/phrase-table.moses.$ext


mapper=createDP-mapper.py
reducer=createDP-reducer.py

name=ComputeDP-$1-$2-$3

mapper_tasks=18
reducer_tasks=36

hadoop fs -mkdir $path_hdfs
expr_date=`date +%Y_%m_%d_%H`

hdfs_input=$path_hdfs/$input_file_name
hdfs_output=$path_hdfs/ComputeDP$ngram.$language

hadoop fs -rm -r $hdfs_output
hadoop fs -copyFromLocal $input_path/monotext/$input_file_name $path_hdfs
hadoop fs -copyFromLocal $output_path/countFreq/$freq_file_name $path_hdfs
#hadoop fs -copyFromLocal $input_dir/stopwords/stopwords.$language $path_hdfs


hadoop jar $jar_file -D mapred.job.name=$name -D mapred.map.tasks=$mapper_tasks -D mapred.reduce.tasks=$reducer_tasks -mapper "\"$mapper $language $remove_stop_words $ngram $numerized\"" -file $mapper -reducer "\"$reducer $language $d $ngram $min_freq $freq_file_name \"" -file $reducer -input $hdfs_input -output $hdfs_output -file $output_path/countFreq/$freq_file_name -file $input_path/stopwords/stopwords.$language $package_str



#hadoop jar $jar_file -D mapreduce.job.name=$name -D mapreduce.job.maps=$mapper_tasks -D mapreduce.job.reduces=$reducer_tasks -mapper "\"$mapper $ngram\"" -file $mapper -reducer $reducer -file $reducer -input $hdfs_input -output $hdfs_output
# check if jobs are done
if [ ! $? -eq 0 ]; then exit $?; fi

mkdir -p $output_path/computeDP
hadoop fs -getmerge "$hdfs_output/part*" $output_path/computeDP/$input_file_name.${ngram}.$expr_date.$language
#hadoop fs -rm $path_hdfs/$input_file_name
echo "Final output is in :$output_path/computeDP/$input_file_name.${ngram}.$expr_date.$language"

