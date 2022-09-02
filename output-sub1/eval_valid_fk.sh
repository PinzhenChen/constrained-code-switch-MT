#! /bin/bash

#for i in fk12 1 2 4 6 12 24 36 48
for i in 1 4 12 24 36 48
do
 echo "evaluating $i"
 #INPUT=valid.output.${i}.hg
 INPUT=./fk_sub1_outputs/valid.marian.hg.beam${i}
 sacrebleu \
  valid.en \
  -i ${INPUT} \
  --chrf-word-order 2 \
  -m bleu chrf ter

 wer valid.en ${INPUT}
done
