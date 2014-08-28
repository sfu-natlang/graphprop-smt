#! /bin/bash
# we have cdec path in Cdec_Path
# and data path in Data_Path


Cdec_Path=/global/scratch/ramtin/software/cdec
#Data_Path=/global/scratch/ramtin/data/parallel_corpora/subtitle_es_en2

source_language_name=en
target_language_name=es

#Train_file_name=OpenSubtitles2013.en-es
#Test_file_name=devtest
#Dev_file_name=dev

#echo "Paste parallel files together \n" > log.log
#Paste parallel files together
#$Cdec_Path/corpus/paste-files.pl $Data_Path/$Train_file_name.$source_language_name $Data_Path/$Train_file_name.$target_language_name > $Data_Path"/training_"$source_language_name"_"$target_language_name

#echo "Preprocessing \n" > log.log
##Preprocessing 

#$Cdec_Path/corpus/tokenize-anything.sh < $Data_Path"/training_"$source_language_name"_"$target_language_name | $Cdec_Path/corpus/lowercase.pl > nc.lc-tok.$source_language_name"-"$target_language_name
#$Cdec_Path/corpus/tokenize-anything.sh < $Data_Path"/dev_"$source_language_name"_"$target_language_name | $Cdec_Path/corpus/lowercase.pl > dev.lc-tok.$source_language_name"-"$target_language_name
#$Cdec_Path/corpus/tokenize-anything.sh < $Data_Path"/devtest_"$source_language_name"_"$target_language_name | $Cdec_Path/corpus/lowercase.pl > devtest.lc-tok.$source_language_name"-"$target_language_name
#$Cdec_Path/corpus/tokenize-anything.sh < "training_"$source_language_name"_"$target_language_name | $Cdec_Path/corpus/lowercase.pl > nc.lc-tok.$source_language_name"-"$target_language_name
#$Cdec_Path/corpus/tokenize-anything.sh < "dev_"$source_language_name"_"$target_language_name | $Cdec_Path/corpus/lowercase.pl > dev.lc-tok.$source_language_name"-"$target_language_name
#$Cdec_Path/corpus/tokenize-anything.sh < "devtest_"$source_language_name"_"$target_language_name | $Cdec_Path/corpus/lowercase.pl > devtest.lc-tok.$source_language_name"-"$target_language_name
#filtering 
# max line lenght 80 
#echo "filtering \n" > log.log
#$Cdec_Path/corpus/filter-length.pl -80 nc.lc-tok.$source_language_name"-"$target_language_name > training.$source_language_name"-"$target_language_name


# bidirectional word alignments
#echo "bidirectional word alignment" > log.log
#$Cdec_Path/word-aligner/fast_align -i training.$source_language_name"-"$target_language_name -d -v -o > training.$source_language_name"-"$target_language_name.fwd_align
#$Cdec_Path/word-aligner/fast_align -i training.$source_language_name"-"$target_language_name -d -v -o -r > training.$source_language_name"-"$target_language_name.rev_align


# Symmetrize word alignments

#$Cdec_Path/utils/atools -i training.$source_language_name"-"$target_language_name.fwd_align -j training.$source_language_name"-"$target_language_name.rev_align -c grow-diag-final-and > training.gdfa



# compile the training data

#python -m cdec.sa.compile -b training.$source_language_name"-"$target_language_name -a training.gdfa -c extract.ini -o training.sa


# Language modeling

#$Cdec_Path/corpus/cut-corpus.pl 2 training.$source_language_name"-"$target_language_name > input_temp_lang
#$Cdec_Path/klm/lm/builder/builder --order 3 <input_temp_lang > nc.lm

#ngram-count -order 3 -text input_temp_lang -lm nc.lm
#$Cdec_Path/klm/lm/build_binary nc.lm nc.klm


#extracting grammars for dev and test

#python -m cdec.sa.extract -c extract.ini -g dev.grammars -j 3 -z < "dev."$source_language_name"-"$target_language_name > dev.lc-tok.$source_language_name"-"$target_language_name.sgm
#python -m cdec.sa.extract -c extract.ini -g devtest.grammars -j 3 -z < "devtest."$source_language_name"-"$target_language_name > devtest.lc-tok.$source_language_name"-"$target_language_name.sgm



# Tunning

python /cs/natlang-user/ramtin/software/cdec-2013-07-13/training/mira/mira.py -d dev.lc-tok.$source_language_name"-"$target_language_name.sgm -t devtest.lc-tok.$source_language_name"-"$target_language_name.sgm -c cdec.ini -j 6

#perl /global/scratch/ramtin/software/cdec/training/dpmert/dpmert.pl -d dev.lc-tok.$source_language_name"-"$target_language_name.sgm -w initweight.ini -c cdec.ini





