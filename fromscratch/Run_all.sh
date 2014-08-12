

#sh countFreq.sh en 2 ../domain/europarl/monotext/ ../domain/europarl/experiments/ monotext.en

#sh computeDP.sh en 2 /cs/natlang-user/ramtin/new_graph/graphprop-smt/domain/europarl/ /cs/natlang-user/ramtin/new_graph/graphprop-smt/domain/europarl/experiments/ monotext.en monotext.en.2.en NOSTOP 0

#sh computeDPNorm.sh /cs/natlang-user/ramtin/new_graph/graphprop-smt/domain/europarl/ /cs/natlang-user/ramtin/new_graph/graphprop-smt/domain/europarl/experiments/ monotext.en.2.2014_08_11_17.en

sh computeInvertedIndex.sh /cs/natlang-user/ramtin/new_graph/graphprop-smt/domain/europarl/ /cs/natlang-user/ramtin/new_graph/graphprop-smt/domain/europarl/experiments/ monotext.en.2.2014_08_11_17.en

