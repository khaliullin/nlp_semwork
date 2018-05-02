from nltk import word_tokenize

from tokenizer import remove_punctuation


def get_words(filename):
    with open(filename) as fin:
        words = word_tokenize(fin.read().lower())
        words = remove_punctuation(words)
    return words
