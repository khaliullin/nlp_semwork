from parser import Parser
from stats import StatsCounter

CORPUS = 'new_corpus'


def main():
    parser = Parser()
    st = StatsCounter()

    l1 = parser.read_corpus(CORPUS)

    reviews = st.count_stats(l1)
    print('Всего отзывов: %s' % reviews)

    words = st.total_words(l1)
    print('Всего слов: %s' % words)

    # Считается довольно долго
    # unique = st.unique_words(l1)
    # print('Уникальных слов: %s' % unique)

    print('Негативных: %s\nПозитивных: %s' % st.negative_positive(l1))

    divided_reviews = parser.divide_by_category(CORPUS)
    n_p_category = st.negative_positive_by_category(divided_reviews)
    print('По категроиям (негативные, поитивные): ')
    print(n_p_category)

    top_negative = st.top_negative(divided_reviews, count=3)
    print(top_negative)

    top_positive = st.top_positive(divided_reviews, count=3)
    print(top_positive)



    # words = get_tokens_for_use('corpus/Аптеки/1_1_1.csv', 'russian')
    # print(words)
    # positive_dictionary = get_words('files/positive.txt')
    # negative_dictionary = get_words('files/negative.txt')
    # pos_count = calculator.count_incoming_word(words, positive_dictionary)
    # neg_count = calculator.count_incoming_word(words, negative_dictionary)
    # print('positive words count =', pos_count)
    # print('negative words count =', neg_count)
    # print('all words count =', len(words))
    # neural_count = len(words) - pos_count - neg_count
    # print('neural words count = ', neural_count)
    # pos_per = calculator.calculate_percentage(pos_count, words)
    # neg_per = calculator.calculate_percentage(neg_count, words)
    # print('positive words percentage =', pos_per)
    # print('negative words percentage =', neg_per)


if __name__ == '__main__':
    main()
