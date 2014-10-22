#!/bin/bash

##### Streaming hadoop library 
jar_file=/usr/lib/hadoop-mapreduce/hadoop-streaming-2.2.0.2.0.6.0-102.jar

#####  input information 
domain=europarl #-20k
lan=en # en fr
direc=$domain-$lan
path_hdfs=/user/rmehdiza/$direc
path_local=/cs/natlang-user/ramtin/new_graph/graphprop-smt/fromscratch
hadoop fs -mkdir $path_hdfs
expr_date=`date +%Y_%m_%d_%H`

##### Graph Creation Types 
graph_type=bi  # bi/tri/full
stopwords=nostop   # nostop
ngram=1
numerized=0 # TODO WHY? 

##### Pruning 
min_freq=0
d=0.3	      	 # DP pruning | d=0 for no limit, 0<d<1 : beam pruning, d>1 histogram pruning
n=15        # n>1: number of neighbors in k-NN, 0<n<1: \epsilon-NN
l=20		 # number of labels per node

if [ $numerized -eq 1 ]; then ext=out.id; else ext=out; fi

#if [ $ngram -gt 1 ]; then ngram_str="-${ngram}gram"; else ngram_str=""; fi

ngram_str=.${ngram}g

if [ $min_freq -gt 0 ]; then freq_str="-rmvFreq$min_freq"; else freq_str=""; fi

#output_dir=$stopwords-d$d$ngram_str$exteq_str-Both

input_dir=/cs/natlang-user/ramtin/new_graph/graphprop-smt/domain/$domain

output_dir=/cs/natlang-user/ramtin/new_graph/graphprop-smt/domain/$domain/experiments

#Created_$expr_date/dp_Ngram-$ngram-Graph-$graph_type-S-$stopword/Prune_minfreq-$min_freq-d-$d-n-$n-l-$l/Propagation_


#countFreq_input=

#dir=$corpus
#output_dir=$stopwords$ngram_str-d$d$freq_str
graph_file=${graph_type}Graph-n${n}
#mkdir -p $dir/$output_dir
reduce_tasks=18

#mkdir -p $path_local/$direc

countFreq()
{
# The first argoman is monotext file name: $1 TODO
 
	mapper=phraseCount-mapper.py
	reducer=phraseCount-reducer.py
	name=phraseCount-$output_dir
	mapper_tasks=18
	reducer_tasks=$reduce_tasks
       
        # loading input
        hadoop fs -copyFromLocal $input_dir/monotext/monotext.$lan $path_hdfs

	input=$path_hdfs/monotext.$lan
	output=$path_hdfs/wordFreq$ngram_str.$lan

	hadoop fs -rm -r $output
	hadoop jar $jar_file -D mapreduce.job.name=$name -D mapreduce.job.maps=$mapper_tasks -D mapreduce.job.reduces=$reducer_tasks -mapper "\"$mapper $ngram\"" -file $mapper -reducer $reducer -file $reducer -input $input -output $output
	if [ ! $? -eq 0 ]; then exit $?; fi
	#hadoop fs -getmerge "$output/part*" $path_local/$direc/wordFreq${ngram_str}.$lan
        mkdir -p $output_dir/countFreq
        hadoop fs -getmerge "$output/part*" $output_dir/countFreq/N${ngram_str}.$expr_date.$lan
}
#countFreq

createDP()
{
# The first argoman is countFreq output: $1
 
    if [ $stopwords = "nostop" ]; then remove_stop_words="true"; else remove_stop_words="false"; fi

	mapper=createDP-mapper.py
	reducer=createDP-reducer.py

	name=createDP-$output_dir
	mapper_tasks=36
	reducer_tasks=$reduce_tasks


        #loading input to hdfs
        hadoop fs -copyFromLocal $input_dir/monotext/monotext.$lan $path_hdfs

	input=$path_hdfs/monotext.$lan
	output=$path_hdfs/DPs 

	hadoop fs -rm -r $output

	hadoop fs -copyFromLocal $input_dir/stopwords/stopwords.$lan $path_hdfs
        #hadoop fs -copyFromLocal phrase-table.moses.$lan $path_hdfs
        #hadoop fs -copyFromLocal oov.$lan $path_hdfs

        #hadoop fs -copyFromLocal phrase-table.moses.out $dir/phrase-table.moses.$ext
        if [ $min_freq -gt 0 ]; then package_str=" -file phrase-table.moses.$lan -file oovs.$lan"; else package_str=""; fi

#	hadoop jar $jar_file -D mapred.job.name=$name -D mapred.map.tasks=$mapper_tasks -D mapred.reduce.tasks=$reducer_tasks -mapper "\"$mapper $lan $remove_stop_words $ngram $numerized\"" -file $mapper -reducer "\"$reducer $lan $d $ngram $min_freq \"" -file $reducer -input $input -output $output -file $path_local/$direc/wordFreq${ngram_str}.$lan -file stopwords.$lan $package_str
	hadoop jar $jar_file -D mapred.job.name=$name -D mapred.map.tasks=$mapper_tasks -D mapred.reduce.tasks=$reducer_tasks -mapper "\"$mapper $lan $remove_stop_words $ngram $numerized\"" -file $mapper -reducer "\"$reducer $lan $d $ngram $min_freq \"" -file $reducer -input $input -output $output -file $1 -file $input_dir/stopwords/stopwords.$lan $package_str


	if [ ! $? -eq 0 ]; then exit $?; fi
	hadoop fs -getmerge "$output/part*" $path_local/$direc/DPs.$lan
}

createDP /cs/natlang-user/ramtin/new_graph/graphprop-smt/domain/europarl/experiments/countFreq/N.1g.2014_08_07_15.en
computeDPNorm()
{
	mapper=identity-mapper.py
	reducer=computeDPNorm-reducer.py
	name=DPNorm-$output_dir
	mapper_tasks=18
	reducer_tasks=$reduce_tasks
        
        #$dir/$output_dir/DPs.$ext

	input=$path_hdfs/DPs/part* 

        hadoop fs -mkdir DPNorm-$output_dir

        output=$path_hdfs/DPNorm-$output_dir  #/labs/natlang/ramtin
	hadoop fs -rm -r $output

	hadoop jar $jar_file -D mapred.job.name=$name -D mapred.map.tasks=$mapper_tasks -D mapred.reduce.tasks=$reducer_tasks -mapper $mapper -file $mapper -reducer $reducer -file $reducer -input $input -output $output
	if [ ! $? -eq 0 ]; then exit $?; fi

	hadoop fs -getmerge "$output/part*" $path_local/$direc/DPNorm.$lan
}

createInvertedIndex()
{
	mapper=createFeatureInvertedIndex-mapper.py
	reducer=createFeatureInvertedIndex-reducer.py
	name=invertedIndex-$output_dir
	mapper_tasks=18
	reducer_tasks=$reduce_tasks
	
        input=$path_hdfs/DPs/part*
	output=$path_hdfs/DPInv-$output_dir  #/labs/natlang/ramtin

        hadoop fs -rm -r $output
	hadoop jar $jar_file -D mapred.job.name=$name -D mapred.map.tasks=$mapper_tasks -D mapred.reduce.tasks=$reducer_tasks -mapper $mapper -file $mapper -reducer $reducer -file $reducer -input $input -output $output
	if [ ! $? -eq 0 ]; then exit $?; fi
	hadoop fs -getmerge "$output/part*" $path_local/$direc/DPInv.$lan
    #python pickle.py $dir/$output_dir/DPInv.$ext
}

constructGraph()
{
	mapper=identity-mapper.py
    #if [ $graph_type = "bi" -o $graph_type = "tri" ]; then reducer=constructGraph-reducer.py; else reducer=constructGraph-reducer.py; fi
	reducer=constructGraph-reducer.py
	name=graphBuilder-$graph_file-$output_dir
	mapper_tasks=36
	reducer_tasks=$reduce_tasks
	input=$path_hdfs/DPs/part* 

        #hadoop fs -copyFromLocal $dir/$output_dir/DPs.$ext /user/rmehdiza/output/DPs-$output_dir/myoutput/

        output=$path_hdfs/$graph_file #-$output_dir  #/labs/natlang/ramtin
        #output=semisup/$dir/$graph_file-$output_dir
	hadoop fs -rm -r $output
	hadoop jar $jar_file -D mapred.task.timeout=240000000 -D mapred.job.name=$name -D mapred.map.tasks=$mapper_tasks -D mapred.reduce.tasks=$reducer_tasks -mapper $mapper -file $mapper -reducer "\"$reducer $lan $n $graph_type \"" -file $reducer -input $input -output $output -file $path_local/$direc/DPInv.$lan -file $path_local/$direc/phrase-table.moses.$lan -file $path_local/$direc/oovs.$lan
	if [ ! $? -eq 0 ]; then exit $?; fi
	hadoop fs -getmerge "$output/part*" $path_local/$direc/$graph_file.$lan
}

constructGraph2Way()
{
 #TODO copy phrase table and oovs

        mapper=identity-mapper.py
    #if [ $graph_type = "bi" -o $graph_type = "tri" ]; then reducer=constructGraph-reducer.py; else reducer=constructGraph-reducer.py; fi
        reducer=constructGraph-reducer-2WayPropagation.py
        name=graphBuilder-$graph_file-$output_dir
        mapper_tasks=36
        reducer_tasks=$reduce_tasks
        input=$path_hdfs/DPs/part*

        #hadoop fs -copyFromLocal $dir/$output_dir/DPs.$ext /user/rmehdiza/output/DPs-$output_dir/myoutput/

        output=$path_hdfs/$graph_file #-$output_dir  #/labs/natlang/ramtin
        #output=semisup/$dir/$graph_file-$output_dir
        hadoop fs -rm -r $output
        hadoop jar $jar_file -D mapred.task.timeout=240000000 -D mapred.job.name=$name -D mapred.map.tasks=$mapper_tasks -D mapred.reduce.tasks=$reducer_tasks -mapper $mapper -file $mapper -reducer "\"$reducer $lan $n $graph_type \"" -file $reducer -input $input -output $output -file $path_local/$direc/DPInv.$lan -file $path_local/$direc/phrase-table.moses.$lan -file $path_local/$direc/oovs.$lan
        if [ ! $? -eq 0 ]; then exit $?; fi
        hadoop fs -getmerge "$output/part*" $path_local/$direc/$graph_file.$lan
}

propagateGraph()
{
echo "-1"
    graph_prop=$graph_file-l${l}
echo "0"
    Temp= $path_local/$direc/$graph_prop
echo $path_local/$direc/$graph_file.$lan
    rm -f $path_local/$direc/$graph_prop.{seeds,graph}
	cat $path_local/$direc/$graph_file.$lan | awk -F"\t" "/\*\*\*/ {print substr(\$1, 4)\"\t|||\"\$2\"|||\t\"\$3  >> \"$path_local/$direc/$graph_prop.seeds\"} ! /\*\*\*/ {print \$0 >> \"$path_local/$direc/$graph_prop.graph\"}"

echo $Temp
	#cat europarl/config | sed -e "s/keep_top_k_labels = .*/keep_top_k_labels = $l/" -e "s/output_file = .*/output_file = $Temp.label_prop_output/" -e "s/graph_file = .*/graph_file =$Temp.graph/" -e "s/seed_file = .*/seed_file = $Temp.seeds/" > $path_local/$direc/$graph_prop.config
	cd $path_local/$direc/
  
echo $path_local/$direc/$graph_prop.config
	junto config $path_local/$direc/$graph_prop.config

echo "4"
    cat $path_local/$direc/$graph_prop.label_prop_output | cut -f1 | python ../map_text.py map.id reverse > tmp1
    cat $path_local/$direc/$graph_prop.label_prop_output | cut -f2- > tmp2
    paste tmp1 tmp2 > $path_local/$direc/$graph_prop.label_prop_output.mapped
    rm -f tmp1 tmp2
	cd -
        echo "Hi"
        #TODO copy information 
	results=`python extract_labels.py $path_local/$direc/$graph_prop.label_prop_output.mapped $path_local/$direc/oovs.dev.out $path_local/$direc/oovs.gold.dev.out $path_local/$direc/phrase-table.moses.out $path_local/$direc/out | tail -n 1`
 
   str="$corpus\t\t$graph_type\t\td=$d\t\tn=$n\t\tl=$l\t\t$results\t\t$path_local/$direc\t\t$graph_prop"
	echo -e $str | tee -a results.txt
    echo -e $str >> $path_local/$direc/result.txt
    for aggreg_type in useForward addForward; do
    	python extract_labels2.py $path_local/$direc/$graph_prop.label_prop_output.mapped $path_local/$direc/oovs.out $path_local/$direc/oovs.gold.out $path_local/$direc/phrase-table.moses.out $path_local/$direc/phrase-table.$aggreg_type.out $aggreg_type 
        echo "***On whole oovs***"
    done
    echo -e "\n$path_local/$direc/$graph_prop"

}



propagateGraph2Way()
{
    graph_file=$graph_file-2way
    graph_prop=$graph_file-Score-l${l}
    rm -f $dir/$output_dir/$graph_prop.{seeds,graph}
	cat $dir/$output_dir/$graph_file.$ext | awk -F"\t" "/\*\*\*/ {print substr(\$1, 4)\"\t|||\"\$2\"|||\t\"\$3  >> \"$dir/$output_dir/$graph_prop.seeds\"} /###/ {print substr(\$1, 4)\"\t|||\"\$2\"|||\t\"\$3  >> \"$dir/$output_dir/$graph_prop.seeds2\"}  ! /\*\*\*|###/ {print \$0 >> \"$dir/$output_dir/$graph_prop.graph\"}"
	cat europarl/config | sed -e "s/keep_top_k_labels = .*/keep_top_k_labels = $l/" -e "s/output_file = .*/output_file = $graph_prop.label_prop_output/" -e "s/graph_file = .*/graph_file = $graph_prop.graph/" -e "s/seed_file = .*/seed_file = $graph_prop.seeds/" > $dir/$output_dir/$graph_prop.config
	cat europarl/config | sed -e "s/keep_top_k_labels = .*/keep_top_k_labels = $l/" -e "s/output_file = .*/output_file = $graph_prop.label_prop_output2/" -e "s/graph_file = .*/graph_file = $graph_prop.graph/" -e "s/seed_file = .*/seed_file = $graph_prop.seeds2/" > $dir/$output_dir/$graph_prop.config2
	cd $dir/$output_dir
	junto config $graph_prop.config
	junto config $graph_prop.config2
    cat $graph_prop.label_prop_output | cut -f1 | python ../../map_text.py ../map.id reverse > tmp1
    cat $graph_prop.label_prop_output | cut -f2- > tmp2
    paste tmp1 tmp2 > $graph_prop.label_prop_output.mapped
    rm -f tmp1 tmp2
    cat $graph_prop.label_prop_output2 | cut -f1 | python ../../map_text.py ../map.id reverse > tmp1
    cat $graph_prop.label_prop_output2 | cut -f2- > tmp2
    paste tmp1 tmp2 > $graph_prop.label_prop_output.mapped2
    rm -f tmp1 tmp2
	cd -
	results=`python extract_labels.py $dir/$output_dir/$graph_prop.label_prop_output.mapped $dir/oovs.dev.out $dir/oovs.gold.dev.out $dir/phrase-table.moses.out $dir/$output_dir/out | tail -n 1`
	#results2=`python extract_labels.py $dir/$output_dir/$graph_prop.label_prop_output.mapped2 $dir/oovs.dev.out $dir/oovs.gold.dev.out $dir/phrase-table.moses.out $dir/$output_dir/out | tail -n 1`
    str="$corpus\t\t$graph_type\t\td=$d\t\tn=$n\t\tl=$l\t\t$results\t\t$dir/$output_dir\t\t$graph_prop"
    #str2="$corpus\t\t$graph_type\t\td=$d\t\tn=$n\t\tl=$l\t\t$results2\t\t$dir/$output_dir\t\t$graph_prop reverse"
	echo -e $str | tee -a results.txt
	#echo -e $str2 | tee -a results.txt
    echo -e $str >> $dir/$output_dir/result.txt
    #echo -e $str2 >> $dir/$output_dir/result.txt
    for aggreg_type in useForward addForward; do
    	python extract_labels2Way.py $dir/$output_dir/$graph_prop.label_prop_output.mapped $dir/oovs.out $dir/oovs.gold.out $dir/phrase-table.moses.out $dir/$output_dir/phrase-table.$graph_prop.$aggreg_type.out $aggreg_type 
    	#python extract_labels2.py $dir/$output_dir/$graph_prop.label_prop_output.mapped2 $dir/oovs.out $dir/oovs.gold.out $dir/phrase-table.moses.out $dir/$output_dir/phrase-table.$graph_file.$aggreg_type.out $aggreg_type 
        echo "***On whole oovs***"
    done
    echo -e "\n$dir/$output_dir/$graph_prop"
}


DP_input=monotext.$ext



#countFreq
#createDP
#createInvertedIndex
#computeDPNorm
#constructGraph
#propagateGraph
#constructGraph2Way
#propagateGraph2Way

