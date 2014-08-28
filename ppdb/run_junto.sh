

hdfs_path=/labs/natlang/ramtin

junto run upenn.junto.graph.parallel.EdgeFactored2NodeFactored \
        junto_config \
        graph_file=europarl_xl_lexical_basic_graph.pruned \
        seed_file=europarl_xl_lexical_seeds.pruned \
        hadoop_graph_file=input_graph_hadoop

hadoop fs -copyFromLocal input_graph_hadoop $hdfs_path/graph_input_xl

#hadoop jar /cs/natlang-projects/users/ramtin/junto-master/target/junto-assembly.jar \
#        upenn.junto.algorithm.parallel.AdsorptionHadoop junto_config

#hadoop jar /cs/natlang-projects/users/ramtin/junto-master/target/junto-assembly.jar \
#       upenn.junto.algorithm.parallel.LP_ZGL_Hadoop junto_config

hadoop jar /cs/natlang-projects/users/ramtin/junto-master/target/junto-assembly.jar \
        upenn.junto.algorithm.parallel.MADHadoop junto_config


#europarl_xxxl_lexical_iter9_propagation_result

hadoop fs -getmerge /labs/natlang/ramtin/graph_output5/_iter_9/part-* final_result_xl
