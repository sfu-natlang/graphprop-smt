

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
fi


hdfs_path=/labs/natlang/ramtin

prefix=$1
#prefix="../ppdb/experiments/europarl_en-es_l_phrasal"
#prefix="../dp/ppdbVsdp/baseline/experiments/Graph/mono.fr.1.2014_11_19_16.fr.2014_11_20_12.graph"

graph_file=$prefix"_basic_graph"
seed_file=$prefix"_seeds"
hadoop_graph_file=$prefix"_hadoop_input_graph"


graph_output=$prefix"_final"

pruned=""
# add .pruned for pruned files

hdfs_input_pattern=/labs/natlang/ramtin/graph_input/
hdfs_output_base=/labs/natlang/ramtin/graph_output/
number_of_iteration="10"

hadoop fs -rmr $hdfs_output_base 
hadoop fs -rmr $hdfs_input_pattern
hadoop fs -mkdir $hdfs_input_pattern

echo "hdfs_input_pattern = $hdfs_input_pattern" > junto_config
echo "hdfs_output_base = $hdfs_output_base" >> junto_config
echo "iters = $number_of_iteration" >> junto_config
echo "mu1 = 1.0" >> junto_config
echo "mu2 = 1e-2" >> junto_config
echo "mu3 = 1e-2" >> junto_config


junto run upenn.junto.graph.parallel.EdgeFactored2NodeFactored \
        junto_config \
        graph_file=$graph_file\
        seed_file=$seed_file  \
        hadoop_graph_file=$hadoop_graph_file



hadoop fs -copyFromLocal $hadoop_graph_file $hdfs_input_pattern

#hadoop jar /cs/natlang-projects/users/ramtin/junto-master/target/junto-assembly.jar \
#        upenn.junto.algorithm.parallel.AdsorptionHadoop junto_config

#hadoop jar /cs/natlang-projects/users/ramtin/junto-master/target/junto-assembly.jar \
#       upenn.junto.algorithm.parallel.LP_ZGL_Hadoop junto_config

hadoop jar /cs/natlang-projects/users/ramtin/junto-master/target/junto-assembly.jar \
        upenn.junto.algorithm.parallel.MADHadoop junto_config


#europarl_xxxl_lexical_iter9_propagation_result

hadoop fs -getmerge $hdfs_output_base"_iter_1/part-*" $graph_output"itr1"
hadoop fs -getmerge $hdfs_output_base"_iter_2/part-*" $graph_output"itr2"

hadoop fs -getmerge $hdfs_output_base"_iter_10/part-*" $graph_output"itr10"

