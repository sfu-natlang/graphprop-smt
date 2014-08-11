# The first argoman is monotext file name: $1 , input directory: $2 , output directory: $3 number of reduce task : $4

#####################################
#Author : Ramtin 
# $1 language
# $2 ngram 
# $3 input directory
# $4 output directory
# $5 monotext file
# $6 number of map (not in use now)
# $7 number of reduce (not in use now)
#####################################

if [ $# -lt 5 ]
  then
    echo "No arguments supplied"
    echo "args: language , ngram , input directory , output directory , monotext file"
    exit 1
fi


##### Streaming hadoop library
jar_file=/usr/lib/hadoop-mapreduce/hadoop-streaming-2.2.0.2.0.6.0-102.jar

#####  input information
path_hdfs=/user/rmehdiza/FreqCount/
language=$1
ngram=$2
input_path=$3
output_path=$4
input_file_name=$5

mapper=phraseCount-mapper.py
reducer=phraseCount-reducer.py
       
name=phraseCount-$1-$2-$3
        
mapper_tasks=18
reducer_tasks=36
        
hadoop fs -mkdir $path_hdfs
expr_date=`date +%Y_%m_%d_%H`


hdfs_input=$path_hdfs/$input_file_name
hdfs_output=$path_hdfs/FreqCount$ngram.$language

hadoop fs -rm -r $hdfs_output
hadoop fs -copyFromLocal $input_path/$input_file_name $path_hdfs

hadoop jar $jar_file -D mapreduce.job.name=$name -D mapreduce.job.maps=$mapper_tasks -D mapreduce.job.reduces=$reducer_tasks -mapper "\"$mapper $ngram\"" -file $mapper -reducer $reducer -file $reducer -input $hdfs_input -output $hdfs_output

# check if jobs are done
if [ ! $? -eq 0 ]; then exit $?; fi

mkdir -p $output_path/countFreq
hadoop fs -getmerge "$hdfs_output/part*" $output_path$input_file_name.${ngram}.$expr_date.$language

#hadoop fs -rm $path_hdfs/$input_file_name 

echo "Final output is in :$output_path$input_file_name.${ngram}.$expr_date.$language" 




