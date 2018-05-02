import calculator
from dictonary_reader import get_words
from tokenizer import get_tokens_for_use


def main():
    words = get_tokens_for_use('corpus/Аптеки/1_1_1.csv', 'russian')
    print(words)
    positive_dictonary = get_words('files/positive.txt')
    negative_dictonary = get_words('files/negative.txt')
    pos_count = calculator.count_incoming_word(words, positive_dictonary)
    neg_count = calculator.count_incoming_word(words, negative_dictonary)
    print('positive words count =', pos_count)
    print('negative words count =', neg_count)
    print('all words count =', len(words))
    neural_count = len(words) - pos_count - neg_count
    print('neural words count = ', neural_count)
    pos_per = calculator.calculate_percentage(pos_count, words)
    neg_per = calculator.calculate_percentage(neg_count, words)
    print('positive words percentage =', pos_per)
    print('negative words percentage =', neg_per)


if __name__ == '__main__':
    main()
