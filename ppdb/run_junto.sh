

#hdfs_path=/labs/natlang/ramtin

#junto run upenn.junto.graph.parallel.EdgeFactored2NodeFactored \
#        junto_config \
#        graph_file=basic_graph \
#        seed_file=seeds \
#        hadoop_graph_file=input_graph_hadoop

#hadoop fs -copyFromLocal input_graph_hadoop $hdfs_path/graph_input

#hadoop jar /cs/natlang-projects/users/ramtin/junto-master/target/junto-assembly.jar \
#        upenn.junto.algorithm.parallel.AdsorptionHadoop junto_config

#hadoop jar /cs/natlang-projects/users/ramtin/junto-master/target/junto-assembly.jar \
#       upenn.junto.algorithm.parallel.LP_ZGL_Hadoop junto_config

#hadoop jar /cs/natlang-projects/users/ramtin/junto-master/target/junto-assembly.jar \
#        upenn.junto.algorithm.parallel.MADHadoop junto_config


hadoop fs -getmerge /labs/natlang/ramtin/graph_output/_iter_9/part-* final_result