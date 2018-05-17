from nltk import SnowballStemmer

# text input
wlist = ['не хороший', 'хороший']

neg_file = open('negative.txt', 'r')
pos_file = open('positive.txt', 'r')
neu_file = open('neutral.txt', 'r')


def count_pos_neg(words_list):
    neg_list = []
    for line in neg_file:
        line = line.strip()
        neg_list.append(line)

    pos_list = []
    for line in pos_file:
        line = line.strip()
        pos_list.append(line)

    neu_list = []
    for line in neu_file:
        line = line.strip()
        neu_list.append(line)

    negative_words = 0
    positive_words = 0
    neutral_words = 0
    words_total = 0

    for word in words_list:
        words_total += 1
        word_with_ne = word.split()
        print(word_with_ne)
        if word_with_ne[0] == "не":
            if word_with_ne[1] in pos_list:
                negative_words += 1
            if word_with_ne[1] in neg_list:
                positive_words += 1
        else:
            if word in neg_list:
                negative_words += 1
            if word in pos_list:
                positive_words += 1
            if word in neu_list:
                neutral_words += 1

    return words_total, positive_words, negative_words, neutral_words


print(count_pos_neg(wlist))