Results
=======

#Name Format

(oov|all) _ (ppdb size) _ (ppdb type) _ (pruning method) _ (number of iterations)

for example 
oov_xl_lexical_bigram_itr9
means we just used propagated values after 9 iteration for oovs not all of rules and graph is constructed based on xl size lexical ppdb and pruned (bigram) 


##Summary

| info | Size | Prune | iteration  | Dev BLEU | Dev TER | Test BLEU | Test TER | 
| ---- | ----- | ------- | ---- | ---- | ------- | ----- | ----- | ------ | ---- |
| baseline | - | - | - | 0.2749 | 0.5448 | 0.2713 | 0.5398 |
| oovs | L | bi | 9 | 0.2750 | 0.5511 | 0.2720 | 0.5462 |
| oovs | XL | bi | 9 | 0.2709 | 0.5499 | 0.2653 | 0.5468 |
| oovs | XL | - | 9 | 0.2748 | 0.5482 | 0.2711 | 0.5429 |
| oovs | XXXL | - | 9 | 0.2722 | 0.5551 | 0.2665 | 0.5512 |
| oovs | XXXL | - | 5 | 0.2696 | 0.5507 | 0.2643 | 0.5458 |
| oovs | XXXL | - | 2 | 0.2744 | 0.5491 | 0.2696 | 0.5458 |
