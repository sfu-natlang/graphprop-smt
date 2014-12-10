


def ngrams(tokens, MIN_N, MAX_N):
    result = []
    n_tokens = len(tokens)
    for i in xrange(n_tokens):
        for j in xrange(i+MIN_N, min(n_tokens, i+MAX_N)+1):
            result.append(" ".join(tokens[i:j]))
    return result


#### check dev
def get_phrases(input):
    dev_phrases = []
    with open(input) as myinp:
        for line in myinp:
            source = line.split("|||")[0]
            dev_phrases = dev_phrases + ngrams(source.split(" "), 1, 7)


    myset = set(dev_phrases)
    for item in myset:
        print item


get_phrases("/cs/natlang-user/ramtin/new_graph/graphprop-smt/domain/europarl/en-es/dev.en-es")
