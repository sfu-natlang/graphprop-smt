#####################################
#Author : Ramtin
# $1 input directory
# $2 output directory
# $3 DP file
# $4 number of map (not in use now) TODO
# $5 number of reduce (not in use now) TODO
#####################################

if [ $# -lt 3 ]
  then
    echo "No arguments supplied"
    echo "args: input directory , output directory , Distribution Profile file"
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


mapper=identity-mapper.py
reducer=computeDPNorm-reducer.py

name=DPNorm-$1-$3
mapper_tasks=18
reducer_tasks=3

hadoop fs -mkdir $path_hdfs
#expr_date=`date +%Y_%m_%d_%H`
expr_date=`date +%Y_%m_%d`

hdfs_input=$path_hdfs/$input_file_name
hdfs_output=$path_hdfs/DPNorm$ngram.$language

hadoop fs -rm -r $hdfs_output
hadoop fs -copyFromLocal $output_path/computeDP/$input_file_name $path_hdfs

hadoop jar $jar_file -D mapred.job.name=$name -D mapred.map.tasks=$mapper_tasks -D mapred.reduce.tasks=$reducer_tasks -mapper $mapper -file $mapper -reducer $reducer -file $reducer -input $hdfs_input -output $hdfs_output
# check if jobs are done
if [ ! $? -eq 0 ]; then exit $?; fi

mkdir -p $output_path/DPNorm
hadoop fs -getmerge "$hdfs_output/part*" $output_path/DPNorm/$input_file_name.$expr_date.norm
#hadoop fs -rm $path_hdfs/$input_file_name

echo "Final output is in :$output_path/DPNorm/$input_file_name.$expr_date.norm"


