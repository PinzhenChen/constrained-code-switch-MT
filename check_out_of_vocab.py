OOVs = []
#TARGET = "valid.gold.hg"
TARGET = "valid.output.fk12.hg"
with open("valid.en") as en_file, open("valid.hi2ht") as hi_file, open(TARGET) as target_file:
    for line_en, line_hi, line_target in zip(en_file, hi_file, target_file):
        vocab = set(line_en.strip().split() + line_hi.strip().split())
        gold_tokens = set(line_target.strip().split())
        not_in_tokens = [t for t in gold_tokens if t not in vocab]
        not_in = len(not_in_tokens)
        total_gold = len(gold_tokens)
        total_vocab = len(vocab)
        OOVs.append([not_in, total_gold, total_vocab, not_in_tokens])

avg = sum(ls[0]*1.0/ls[1] for ls in OOVs) / len(OOVs)
print(avg)
for i in range(5):
    print(OOVs[i][3])
