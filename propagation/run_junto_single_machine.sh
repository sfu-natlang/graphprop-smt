

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
fi


prefix=$1
#prefix="../ppdb/experiments/europarl_en-es_l_phrasal"
#prefix="../dp/ppdbVsdp/baseline/experiments/Graph/mono.fr.1.2014_11_19_16.fr.2014_11_20_12.graph"

graph_file=$prefix"_basic_graph"
seed_file=$prefix"_seeds"
hadoop_graph_file=$prefix"_hadoop_input_graph"


graph_output=$prefix"_final"

pruned=""
# add .pruned for pruned files

number_of_iteration="5"


echo "graph_file = $graph_file" > junto_config
echo "data_format = edge_factored" >> junto_config
echo "seed_file = $seed_file" >> junto_config

echo "verbose = false" >> junto_config
echo "prune_threshold = 0" >> junto_config
echo "algo = mad" >> junto_config
echo "iters = $number_of_iteration" >> junto_config
echo "mu1 = 1.0" >> junto_config
echo "mu2 = 1e-2" >> junto_config
echo "mu3 = 1e-2" >> junto_config
echo "beta = 2" >> junto_config
echo "output_file = $graph_output" >> junto_config

junto config junto_config

