
timestamp='2014_10_07_15'
filename='europarl_v7-1k.en'

sh countFreq.sh en 2 ../domain/europarl/monotext/ ../domain/europarl/experiments/ europarl_v7-1k.en

#sh computeDP.sh en 2 /cs/natlang-user/ramtin/new_graph/graphprop-smt/domain/europarl/ /cs/natlang-user/ramtin/new_graph/graphprop-smt/domain/europarl/experiments/ $filename $filename.2.$timestamp.en NOSTOP 0

#sh computeDPNorm.sh /cs/natlang-user/ramtin/new_graph/graphprop-smt/domain/europarl/ /cs/natlang-user/ramtin/new_graph/graphprop-smt/domain/europarl/experiments/ $filename.2.$timestamp.en

#sh computeInvertedIndex.sh /cs/natlang-user/ramtin/new_graph/graphprop-smt/domain/europarl/ /cs/natlang-user/ramtin/new_graph/graphprop-smt/domain/europarl/experiments/ $filename.2.$timestamp.en

sh constructGraph.sh /cs/natlang-user/ramtin/new_graph/graphprop-smt/domain/europarl/en-es/ /cs/natlang-user/ramtin/new_graph/graphprop-smt/domain/europarl/experiments/ $filename.2.$timestamp.en bi 15 $filename.2.$timestamp.en.$timestamp.indx en temp.en oovs.dev.en

# phrase-table.moses.en 



