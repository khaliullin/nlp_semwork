import nltk
from nltk import SnowballStemmer
from nltk.corpus import stopwords

import parser

languages = ['english', 'russian']


def get_token(filename):
    text = parser.read_csv(filename)['text'].lower()
    words = nltk.word_tokenize(text)
    return words


def remove_punctuation(tokens):
    words = [word for word in tokens if word.isalpha()]
    return words


def remove_stopwords(tokens, lang):
    if languages.__contains__(lang):
        filtered_words = [word for word in tokens if word not in stopwords.words(lang)]
        return filtered_words
    return tokens


def stem(tokens, lang):
    if languages.__contains__(lang):
        snowball = SnowballStemmer(lang)
        stemmed = []
        for word in tokens:
            stemmed.append(snowball.stem(word))
        return stemmed
    return tokens


def get_tokens_for_use(filename, lang):
    tokens = get_token(filename)
    without_punctuation = remove_punctuation(tokens)
    without_stop_words = remove_stopwords(without_punctuation, lang)
    stemmed = stem(without_stop_words, lang)
    return without_punctuation
