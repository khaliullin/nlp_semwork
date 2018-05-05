import math

ebs = 0.0001


def unigram_dict(words):
    d = dict()
    for word in words:
        if word in d.keys():
            d[word] += 1
        else:
            d[word] = 1

    return d


def unigram_freq(dictionary):
    frequency_dict = dict()
    for word in dictionary:
        frequency_dict[word] = dictionary[word] / len(dictionary)
    return frequency_dict


def bigram_freq(all_words, unigram_dict):
    data_str = ' '.join(all_words)
    all_words = list(enumerate(all_words))

    frequencies = dict()

    for ind, i in all_words:
        for j in range(ind, len(all_words)):
            i2 = all_words[j][1]
            pair = '%s %s' % (i, i2)
            val = data_str.count(pair) / unigram_dict[i]
            if (i, i2) in frequencies.keys():
                if frequencies[(i, i2)] < val:
                    frequencies[(i, i2)] = val
            else:
                frequencies[(i, i2)] = val
    return frequencies


def pmi(unigram_freq, bigram_freq):
    pmi_dict = dict()
    for key in bi_freq.keys():
        word1 = key[0]
        word2 = key[1]
        prob_word1 = unigram_freq[word1] / float(sum(unigram_freq.values())) + ebs
        prob_word2 = unigram_freq[word2] / float(sum(unigram_freq.values())) + ebs
        prob_word1_word2 = bigram_freq[(word1, word2)] / float(sum(bigram_freq.values())) + ebs
        pmi_dict[(word1, word2)] = math.log(prob_word1_word2 / float(prob_word1 * prob_word2), 2)
    return pmi_dict


if __name__ == '__main__':
    words = []
    unigram_d = unigram_dict(words)
    uni_freq = unigram_freq(unigram_d)
    bi_freq = bigram_freq(words, unigram_d)
    pmi_freq = pmi(uni_freq, bi_freq)
    print(unigram_d)
    print(uni_freq)
    print(bi_freq)
    print(pmi_freq)
