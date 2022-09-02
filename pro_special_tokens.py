#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 04:12:38 2022

@author: fkirefu
"""
# from ai4bharat.transliteration import XlitEngine
import sys
import re
import random
import argparse, json
from collections import defaultdict
import ast

# parser = argparse.ArgumentParser()
# parser.add_argument("-d", "--download-remove", action="store_true",
#                     help="filters out most of the download sentences", default=False)

HASHTAG = "<HT>"
THANDLE = "<TH>"
URL = "<URL>"
EMO = "<ST9>"
FILTER_VAL = 0.4

SPECIALS = [HASHTAG, THANDLE, URL, EMO]


parser = argparse.ArgumentParser(description="Preprocessing and postprocessing script")

# main parameters
parser.add_argument("--task", type=str, default="pre", help="pre or post")
parser.add_argument("--set", type=str, default="valid", help="train, valid or test")
parser.add_argument("--input_file", type=str)

parser.add_argument("--save_tok", type=str, help="Save output")
parser.add_argument("--save_place_holder_file", type=str, help="Save_place_holder")
parser.add_argument("--read_place_holder_file", type=str, help="read place holder_file")
parser.add_argument(
    "--source_file", type=str, help="HG source file for post processing"
)
parser.add_argument(
    "--save_detok",
    type=str,
    help="Final English detokenised source file for post processing",
)

EMOJI_PATTERN_1 = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "\U000024C2-\U0001F251"
    "]+",
    flags=re.UNICODE,
)


# EMOJI_PATTERN_2 = re.compile("(\u00a9|\u00ae|[\u2000-\u3300]|\ud83c[\ud000-\udfff]|\ud83d[\ud000-\udfff]|\ud83e[\ud000-\udfff])", flags=re.UNICODE)

# EMOJI_PATTERN = re.compile("/(\u00a9|\u00ae|[\u2000-\u3300]|\ud83c[\ud000-\udfff]|\ud83d[\ud000-\udfff]|\ud83e[\ud000-\udfff])/gi", flags=re.UNICODE)


# except UnicodeDecodeError as err:

#     print("<PROBLEM_FILT>")
#     continue


def tokenise_sent(sent_list):
    sp_tok_dict = defaultdict(list)
    new_sent_list = []
    #    if "ownload" in sent.lower():
    #        if random.random() > 0.01: continue # filtering download

    for ind, w in enumerate(sent_list):
        # if not w: continue
        orig_w = w
        low_w = w.lower()
        # filter hash tags

        if w.startswith("#"):
            w = HASHTAG
            sp_tok_dict[HASHTAG].append((ind, orig_w))

        # filter twitter handles

        elif w.startswith("@"):
            w = THANDLE
            sp_tok_dict[THANDLE].append((ind, orig_w))

        elif (
            "www." in low_w
            or "http" in low_w
            or ".com" in low_w
            or ".html" in low_w
            or "url" == low_w
        ):
            w = URL
            sp_tok_dict[URL].append((ind, orig_w))

        elif EMOJI_PATTERN_1.match(w):

            if "–" in orig_w:
                w = orig_w
            else:

                w = EMO
                sp_tok_dict[EMO].append((ind, orig_w))

        new_sent_list.append(w)

    assert len(new_sent_list) == len(sent_list)

    new_sent = " ".join(new_sent_list)

    sp_count = new_sent.count(HASHTAG)
    sp_count += new_sent.count(THANDLE)
    sp_count += new_sent.count(URL)
    sp_count += new_sent.count(EMO)

    sp_tok_dict_total = sum([len(v) for v in sp_tok_dict.values()])

    # print(sent_list)
    # print(new_sent)
    # print()
    # print(sp_tok_dict_total, sp_count, sp_tok_dict)
    assert sp_count == sp_tok_dict_total

    return new_sent, sp_tok_dict

    # if not count/len(new_sent) > FILTER_VAL:
    # print(" ".join(new_sent))


# sys.stdin.reconfigure(encoding='utf-8', errors='replace')


def tokenise_train(params):

    assert params.input_file
    assert params.save_tok
    assert params.task == "pre"

    with open(params.input_file, "r", encoding="utf8", errors="ignore") as f:
        with open(params.save_tok, "w") as save:

            try:
                for ind, sent in enumerate(f):

                    sent_list = [a for a in sent.strip().split(" ") if a]
                    new_sent, default = tokenise_sent(sent_list)
                    save.write("{}\n".format(new_sent))
                    # print(ind, sent)
            except UnicodeDecodeError as e:

                print(ind, sent)
                pass
                # sys.exit(55)


def tokenise_valid(params):

    assert params.input_file
    assert params.save_tok
    assert params.task == "pre"

    with open(params.input_file, "r") as f:
        with open(params.save_tok, "w") as save:
            with open(params.save_place_holder_file, "w") as place:

                for sent in f:

                    sent_list = [a for a in sent.strip().split(" ") if a]
                    new_sent, default = tokenise_sent(sent_list)
                    save.write("{}\n".format(new_sent))
                    place.write("{}\n".format(json.dumps(default)))


def substitue_back(params):

    assert params.read_place_holder_file
    assert params.source_file
    assert params.save_detok
    assert params.read_place_holder_file

    with open(params.input_file, "r") as f:
        with open(params.source_file, "r") as srcf:
            with open(params.save_detok, "w") as save:
                with open(params.read_place_holder_file, "r") as place:

                    for tgt_sent, line, src in zip(f, place, srcf):
                        proc_tgt = tgt_sent.strip()
                        sp_tok_dict = ast.literal_eval(line.strip())

                        # no subs to be made
                        if not sp_tok_dict:

                            for sp in SPECIALS:
                                proc_tgt = proc_tgt.replace(sp, "")

                        else:
                            
                            tgt_sent_list = proc_tgt.split(' ')
                            new_tgt_sent_list = list(tgt_sent_list)
                            for spr in SPECIALS:
                                
                                try:
                                    vals = sp_tok_dict[spr]
                                except KeyError:
                                    vals = []
                                    new_tgt_sent_list = [b for b in new_tgt_sent_list if spr not in b] # filter out any special tokens present, don't care
                                    proc_tgt = " ".join(new_tgt_sent_list)
                                
                                
                                # WHEN OUTPUT HAS MATCHED EXPECTED NUMBER OF TOKENS
                                if len(vals) == proc_tgt.count(spr):
                                    i = 0
                                    to_loop = list(new_tgt_sent_list)
                                    for en, w in enumerate(to_loop):
                                        if spr in w:
                                            
                                            split_spr = w.split(spr)
                                            assert len(split_spr) == 2
                                            split_before = split_spr[0]
                                            split_after = split_spr[1]

                                            
                                            w = split_before+ sp_tok_dict[spr][i][1] + split_after
                                            i += 1
                                        new_tgt_sent_list[en] = w
                                    
                                    assert i == len(vals)
                                
                                else:

                                    tgt_indices_orig = [k for k ,x in enumerate(tgt_sent_list) if spr in x ]
                                    tgt_indices_dict = {}
                                    must_insert = []
                                    tgt_indices_to_pop = [k for k ,x in enumerate(tgt_sent_list) if  spr in x ]
                                    
                                    src_indices = {m[0]:m[1] for m in sp_tok_dict[spr] }
                                    
                                    for s_i, to_sub in src_indices.items():
                                        
                                        if tgt_indices_to_pop:
                                            
                                            tgt_indices_dict[tgt_indices_to_pop[0]] = to_sub
                                            tgt_indices_to_pop = tgt_indices_to_pop[1:]
                                            print("here33", s_i, to_sub )

                                        else:
                                            print("here", s_i, to_sub )
                                            must_insert.append((s_i, to_sub))
                                    
                                    print("ind_dict", tgt_indices_dict)
                                    for kk, vv in tgt_indices_dict.items():
                                        
                                        old_cand = new_tgt_sent_list[kk]
                                        
                                        split_spr = old_cand.split(spr)
                                        #print(split_spr)
                                        assert len(split_spr) == 2
                                        split_before = split_spr[0]
                                        split_after = split_spr[1]
                                        
                                        new_tgt_sent_list[kk] = vv
                                    
                                    if tgt_indices_to_pop:
                                         new_tgt_sent_list = [ww for ww in new_tgt_sent_list if spr not in ww]
                                        
                                    # now account for any items not left
                                    for tup in must_insert:
                                        
                                        for cand in new_tgt_sent_list:
                                            assert tup[1] not in cand
                                        
                                        if tup[0] >= len(new_tgt_sent_list):
                                            new_tgt_sent_list.append(tup[1])
                                        else:
                                            new_tgt_sent_list = new_tgt_sent_list[:tup[0]] + [tup[1]] + new_tgt_sent_list[tup[0]:]
                                    
                                        
      
                            
                            
                            proc_tgt = " ".join(new_tgt_sent_list)
                        # final checls
                        for sp, tup_list in sp_tok_dict.items():
                            # all special tokens have been replaced
                            assert sp not in proc_tgt
                            
                            for tup in tup_list:            
                                
                                # all things from  dictionary are in the output
                                assert tup[1] in proc_tgt
                            
                        print()
                        print(proc_tgt)
                        print(tgt_sent)
                        print(src)
                        print(sp_tok_dict)
                        
                        save.write("{}\n".format(proc_tgt))
                        print()

                                
                                # else:
                                    
                                #     assert len(vals) < proc_tgt.count(spr)

                                # try:
                                #     assert len(vals) == proc_tgt.count(spr)
                                # except AssertionError:
                                #     print(spr, len(vals))
                                #     print(src)
                                #     print(proc_tgt)
                                #     print()
                                #     print()
                                #     continue

                        # sent_list = [a for a in sent.strip().split(' ') if a]
                        # new_sent, default = tokenise_sent(sent_list)
                        # save.write("{}\n".format(new_sent))
                        # place.write("{}\n".format(json.dumps(default)))


if __name__ == "__main__":

    params = parser.parse_args()

    if params.task == "pre":

        if params.set == "train":
            tokenise_train(params)
        else:
            tokenise_valid(params)
            assert params.save_place_holder_file
    else:

        assert params.task == "post"

        substitue_back(params)
