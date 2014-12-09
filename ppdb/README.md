# Graph Construction Using PPDB
Using ppdb prapharses for solving out of vocabulary problem in SMT.
##dependencies : 
* Cdec
* Junto

## Running the code
  For running the code you need to pass parameters to command.py and these parameters are size , type and language of ppdb and domain path of input data
  e.g. `python command.py xl en lexical europarl`
 

##Classes in the directory
* Processor
This class is located in ppdb_processor file and is responsible for processing ppdb files and change it to the graph file format which can be used in the next steps. It uses a dictonary to set id for phrases (or lexicals) and store the mapping between phrases and ids as a python dictionary object. This file also provide useful statistical information about selected PPDB file.

* Labeler
This class is located in add_label_to_graph and is responsible for sending each phrase to CDEC grammar extractor and appending corresponding labels to the seed nodes.

* Pruner
This can be used to prune the graph in different ways. Right now it support bigram and trigram, KNN pruning and also radius pruning.

Note that all of these classes has their own unit test in their corresponding files.

## Other Files
* grammar_appending.py 
For extracting new rules and appending them to the previous rules, this file is useful.

## Multi language graph construction
Files starts with multi are multi-langauge version of the previous files. Note that the structure of stroing is different from before.


TODO : Explain the Structure of storing



