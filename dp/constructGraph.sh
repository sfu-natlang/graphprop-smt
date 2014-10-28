#####################################
#Author : Ramtin
# $1 input directory
# $2 output directory
# $3 DP file
# $4 graphtype  (bi/tri/full)
# $5 n>1: number of neighbors in k-NN, 0<n<1: \epsilon-NN
# $6 DP inv file
# $7 language
# $8 phrase table 
# $9 OOV file
# $10 number of map (not in use now) TODO
# $11 number of reduce (not in use now) TODO
#####################################

if [ $# -lt 9 ]
  then
    echo "No arguments supplied"
    echo "args: input directory , output directory , Distribution Profile file, graph type, neighbour info, DP inverted Index, Language, phrase table, oov file"
    exit 1
fi

##### Streaming hadoop library
#jar_file=/usr/lib/hadoop-mapreduce/hadoop-streaming-2.2.0.2.0.6.0-102.jar
jar_file=/usr/lib/hadoop-mapreduce/hadoop-streaming.jar

#####  input information
path_hdfs=/user/rmehdiza/computeDPNorm/
input_path=$1
output_path=$2
input_file_name=$3
graph_type=$4
n=$5
DP_Inv_File=$6
language=$7
phrase_table_file=$8
oov_file=$9

mapper=identity-mapper.py
reducer=constructGraph-reducer.py

name=graphBuilder-$1-$3
mapper_tasks=18
reducer_tasks=36

hadoop fs -mkdir $path_hdfs
expr_date=`date +%Y_%m_%d_%H`

hdfs_input=$path_hdfs/$input_file_name
hdfs_output=$path_hdfs/Graph_$3

hadoop fs -rm -r $hdfs_output
hadoop fs -copyFromLocal $output_path/computeDP/$input_file_name $path_hdfs

hadoop jar $jar_file -D mapred.task.timeout=240000000 -D mapred.job.name=$name -D mapred.map.tasks=$mapper_tasks -D mapred.reduce.tasks=$reducer_tasks -mapper $mapper -file $mapper -reducer "\"$reducer $language $n $graph_type 100 $output_path/computeInvIndx/$DP_Inv_File $input_path/$phrase_table_file $input_path/$oov_file\"" -file $reducer -input $hdfs_input -output $hdfs_output -file $output_path/computeInvIndx/$DP_Inv_File -file $input_path/$phrase_table_file -file $input_path/$oov_file

# check if jobs are done
if [ ! $? -eq 0 ]; then exit $?; fi

mkdir -p $output_path/Graph
hadoop fs -getmerge "$hdfs_output/part*" $output_path/Graph/$input_file_name.$expr_date.graph
#hadoop fs -rm $path_hdfs/$input_file_name

echo "Final output is in :$output_path/Graph/$input_file_name.$expr_date.graph"


 
