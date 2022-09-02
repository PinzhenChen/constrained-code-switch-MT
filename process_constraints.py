from collections import defaultdict

VOCAB_FILE="/path/to/vocab.yml"

split="test"
HI_FILE="/path/to/sub1.bpe.hi".format(split)
HT_FILE="/path/to/sub1.bpe.ht".format(split)
EN_FILE="/path/to/sub1.bpe.en".format(split)
#HG_FILE="/path/to/unconstrained.decoded.hg.raw".format(split)

split="valid"
HI_FILE="/path/to/valid.hi.bpe"
HT_FILE="/path/to/valid.hi2ht.bpe"
EN_FILE="/path/to/valid.en.bpe"

HI_CHAR_SET=list("ऀँंःऄअआइईउऊऋऌऍऎएऐऑऒओऔकखगघङचछजझञटठडढणतथदधनऩपफबभमयरऱलळऴवशषसहऺऻ़ऽाि ीुूृॄॅॆेैॉॊोौ्ॎॏॐ॒॑॓॔ॕॖॗक़ख़ग़ज़ड़ढ़फ़य़ॠॡॢॣ।॥०१२३४५६७८९॰ॱॲॳॴॵॶॷॸॹॺॻॼॽॾॿ")
SPECIAL_TOKENS={"<unk>", "<BT>", "<HT>", "<TH>", "<URL>", "<ST1>", "<ST2>", "<ST3>", "<ST4>", "<ST5>", "<ST6>", "<ST7>", "<ST8>", "<ST9>"}

OUTPUT="/path/to/constraint/output/"

"""
    parse a vocab file into a dict
"""
def process_vocab(input_file):

    def defaultdict_value():
        return "0"
    vocab_dict = defaultdict(defaultdict_value)

    with open(input_file, "r") as vocab_file:
        for line in vocab_file:
            token, id = line.strip().split(": ")
            vocab_dict[token.replace('"' , "")] = id
    return vocab_dict


"""
    read input files, and generate a list of constraints for each line
"""
def generate_constraints(input_hi, input_ht, input_en, vocab_dict, hi_chars=HI_CHAR_SET):
    constraints = []
    with open(input_hi) as hi_file, open(input_ht) as ht_file, open(input_en) as en_file:
        #assert len(hi_file) == len(ht_file) == len(en_file), "the input files should have the same number of lines"
        for line_hi, line_ht, line_en in zip(hi_file, ht_file, en_file):
            hi_tokens = [sw for sw in line_hi.strip().split() if not any(c in sw for c in hi_chars)]
            ht_tokens = line_ht.strip().split()
            en_tokens = line_en.strip().split()
            # hg_tokens = line_hg.strip().split()

            hi_ids = [vocab_dict[c] for c in hi_tokens if c not in SPECIAL_TOKENS]
            ht_ids = [vocab_dict[c] for c in ht_tokens if c not in SPECIAL_TOKENS]
            en_ids = [vocab_dict[c] for c in en_tokens if c not in SPECIAL_TOKENS]
            # hg_ids = [vocab_dict[c] for c in en_tokens if c not in SPECIAL_TOKENS]

            # constraints.append(set(hi_ids + ht_ids + en_ids + hg_ids + ["0"])) # always allow </s>
            constraints.append(set(hi_ids + ht_ids + en_ids + ["0"])) # always allow </s>
    return constraints


def create_input_lines(input_file, output_file_prefix):
    with open(input_file) as file:
        for i, line in enumerate(file):
            #with open(output_file_prefix + "_" + str(i) + "." + input_file.split(".")[-1], "w") as output_file:
            with open(output_file_prefix + "_" + str(i) + "." + input_file.split(".")[-2], "w") as output_file:
                output_file.write(line)


def write_to_file(constraints, output_file_prefix):
    for i, constraint in enumerate(constraints):
        with open(output_file_prefix + "_" + str(i), "w") as output_file:
            for id in constraint:
                output_file.write(str(id) + "\n")


if __name__ == "__main__":
    vocab_dict = process_vocab(input_file=VOCAB_FILE)
    constraints = generate_constraints(input_hi=HI_FILE,
                                        input_ht=HT_FILE,
                                        input_en=EN_FILE,
                                        vocab_dict=vocab_dict,
                                        )
    write_to_file(constraints, output_file_prefix=OUTPUT)
    create_input_lines(HI_FILE, output_file_prefix=OUTPUT)
    create_input_lines(EN_FILE, output_file_prefix=OUTPUT)
