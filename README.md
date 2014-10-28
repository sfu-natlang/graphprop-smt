graphprop-smt
=============
Graph propagation for statistical machine translation


#Directory Structure

## PPDB
Using ppdb for parapharsing

## DP
Using distributional profile and cosine similarity extracted from monolingual text

## Domain
input data for SMT 

## Reports 
Storing logs and results of experiments
 


#Graph file formats
Using both DP and PPDB would result in these files that are used in propagation section

### input graph
(name_of_node) \<tab\> (name_of_neighbour_node) \<tab\> (weight) \<newline\>

### gold labels
(name_of_node) \<tab\> (label) \<tab\> (prob) \<newline\>

### seeds
(name_of_node) \<tab\> (label) \<tab\> (prob) \<newline\>


#Propagation Methods 

### MAD

### MADLL


# Merging Methods 

Just oovs, smoothing (lexical, phrasal)


<pre>
                     Files
  +---------+      +---------+      +-----------+       +-------------+
  |Step 1   |      |graph inp|      |Propagation|       |   Merge     |
  |---------|      +---------+      |-----------|       |-------------|
  | PPDB    |+---->|Seeds    |+---->|Simple     |+----->|OOVs lexical |
  | DP      |      +---------+      |MAD        |       |Smoothing phr|
  |         |      |Golden   |      |MADLL      |       |             |
  +---------+      +---------+      +-----------+       +-------------+
</pre>
