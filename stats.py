import nltk

from tokenizer import remove_punctuation


class StatsCounter:

    @staticmethod
    def count_stats(reviews_list):
        return len(reviews_list)

    @staticmethod
    def total_words(reviews_list):
        count = 0
        for review in reviews_list:
            count += len(review['text'].split())
        return count

    @staticmethod
    def unique_words(reviews_list):
        all_words = []
        for review in reviews_list:
            tokens = nltk.word_tokenize(review['text'].lower())
            no_pun = remove_punctuation(tokens)
            all_words.extend(no_pun)
        return len(set(all_words))
