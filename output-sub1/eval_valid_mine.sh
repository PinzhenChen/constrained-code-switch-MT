#! /bin/bash

for i in 1 2 4 6 12 24 36 48
do
 echo "evaluating $i"
 INPUT=valid.output.${i}.hg
 sacrebleu \
  valid.hi2ht \
  -i ${INPUT} \
  --chrf-word-order 2 \
  -m bleu chrf ter

 wer valid.en ${INPUT}
done
