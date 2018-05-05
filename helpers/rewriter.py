"""
Переписывает корпус из разных файлам в один, разделяя по направлениям
"""
import csv
import os

import pandas as pd

CORPUS_PATH = '../corpus'   # входной корпус
NEW_CORPUS_PATH = '../new_corpus/'  # выход


def read_corpus(corpus, new_corpus):
    # Создаем папку
    if not os.path.exists(new_corpus):
        os.makedirs(new_corpus)

    folders = os.listdir(corpus)
    for folder in folders:
        if not folder.startswith("."):
            print(folder)
            with open(new_corpus + folder + '.csv', 'w') as out_file:
                writer = csv.writer(out_file, delimiter='\t', quotechar='|', quoting=csv.QUOTE_ALL)

                for review in os.listdir(os.path.join(corpus, folder))[:-2]:
                    print('\t' + review)
                    review_path = os.path.join(corpus, folder, review)
                    reader = list(csv.reader(open(review_path, newline='\n'), delimiter='\n'))
                    title = reader[0][0]
                    text = ' '.join(str(review) for paragraph in reader[1:] for review in paragraph)
                    is_positive = review[-5]
                    writer.writerow([title] + [text] + [is_positive])


if __name__ == '__main__':
    read_corpus(CORPUS_PATH, NEW_CORPUS_PATH)