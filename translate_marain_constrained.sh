#!/bin/bash

# MUST CHANGE INPUTS IN THIS FILE
master_yml=/path/to/config.yml
tmp_yml=/path/to/tmp.yml

MOSES=/path/to/mosesdecoder
detokenizer=$MOSES/scripts/tokenizer/detokenizer.perl
tokenizer=$MOSES/scripts/tokenizer/tokenizer.perl

another_tmp_dir=/path/to/tmp_files
tmp_file_dir="\/path\/to\/tmp_files"

MARIAN_DECODER=/path/to/marian-decoder

python3 /path/to/process_constraints.py

for beamsize in 6
do
 for num in {0..499}
 do
  hi_path="$tmp_file_dir\/temp_${num}.hi"
  en_path="$tmp_file_dir\/temp_${num}.en"

  cat $master_yml | sed "s/REP4HI/${hi_path}/g" | sed "s/REP4EN/${en_path}/g"  > $tmp_yml
  outputpath=$another_tmp_dir/temp_${num}.${beamsize}.valid.hg
  cp $another_tmp_dir/temp_${num} $another_tmp_dir/temp_constraint

  $MARIAN_DECODER -c $tmp_yml -b $beamsize -n 1 --cpu-threads 1 \
        --mini-batch 1 --max-length-crop --maxi-batch 1  --maxi-batch-sort src \
        | sed -r 's/(@@ )|(@@ ?$)//g' | $detokenizer -l en > $outputpath
 done
done
