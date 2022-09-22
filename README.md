# Code-switching Translation with Constrained Decoding.

This repository contains Marian NMT beam search code that supports decoding constrained to source sentence(s). During decoding, the output vocabulary is restricted to the tokens that appear in the input source(s).

The motivation is that when translating into a code-switched language (from English and Hindi to "Hinglish" in our case), the target side words should come from the sources regardless of languages (e.g. any "Hinglish" words should be from either English or Hindi transliterated into English). We find that transliteration of words in different languages might cause error propagation. ``output-sub1/`` contains constrained and unconstrained outputs with different beam sizes for your eyes.

This was intended for Edinburgh's submission to code-switched translation shared task (MixMT) at WMT 2022. Generic stuff like the model, vocab, and outputs were originally developed by Faheem Kirefu.
