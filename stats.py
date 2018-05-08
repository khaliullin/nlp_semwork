import operator

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

    @staticmethod
    def negative_positive(reviews_list):
        negative = 0
        positive = 0
        for review in reviews_list:
            if review['positive']:
                positive += 1
            else:
                negative += 1
        return negative, positive

    @staticmethod
    def negative_positive_by_category(reviews_list_divided):
        direction_result = dict()
        for direction in reviews_list_divided:
            negative = 0
            positive = 0
            for review in direction[1]:
                if review['positive']:
                    positive += 1
                else:
                    negative += 1
            direction_result.update({direction[0][:-4]: (negative, positive)})
        return direction_result

    def top_negative(self, reviews_list_divided, count=None):
        neg_pos = self.negative_positive_by_category(reviews_list_divided)
        ratio = {}
        for category in neg_pos:
            ratio.update({category: neg_pos[category][0]/neg_pos[category][1]})
        sorted_ratio = sorted(ratio.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_ratio[:count]

    def top_positive(self, reviews_list_divided, count=None):
        neg_pos = self.negative_positive_by_category(reviews_list_divided)
        ratio = {}
        for category in neg_pos:
            ratio.update({category: neg_pos[category][0]/neg_pos[category][1]})
        sorted_ratio = sorted(ratio.items(), key=operator.itemgetter(1))
        return sorted_ratio[:count]
