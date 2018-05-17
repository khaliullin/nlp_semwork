from nltk import SnowballStemmer

dictionary_path = "rusentilex.txt"

neg_file = open('negative.txt', 'w')
pos_file = open('positive.txt', 'w')
neu_file = open('neutral.txt', 'w')


def parse_mixed_dict(dictionary_path):
    with open(dictionary_path, 'r') as file:
        for line in file:
            line = line.strip()
            arr = line.split(",")
            word = arr[2].strip()
            # word = SnowballStemmer('russian').stem(word)
            print(word)
            sentiment = arr[3].strip()
            # print(sentiment)

            if sentiment == 'negative':
                neg_file.write(word + '\n')
            if sentiment == 'positive':
                pos_file.write(word + '\n')
            if sentiment == 'positive/negative':
                pos_file.write(word + '\n')
                neg_file.write(word + '\n')
            if sentiment == 'neutral':
                neu_file.write(word + '\n')


parse_mixed_dict(dictionary_path)


