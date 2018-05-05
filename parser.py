import csv
import glob
import os

CORPUS = 'new_corpus'


def read_csv(filename, limit=None):
    """
    Возвращает словарь {'title', 'text', 'positive'}
    """
    reviews_list = []
    reader = csv.reader(open(filename, newline='\n'), delimiter='\t', quotechar='|')
    for record in list(reader)[:limit]:
        reviews_list.append({'title': record[0], 'text': record[1], 'positive': record[2] == '1'})
    return reviews_list


def read_corpus(corpus, direction_name='', limit=None):
    """
    :param corpus: Строка с названием папки корпуса (Обязательный параметр)
    :param direction_name: Конкретный файл с отзывами (прим. 'Больницы')
    :param limit: Количество читаемых отзывов из файлов
    :return: Список со словарями отзывов
    """
    reviews_list = []
    if direction_name:
        filename = os.path.join(corpus, direction_name + '.csv')
        return read_csv(filename, limit)
    else:
        folder = os.listdir(corpus)
        for file in folder:
            if not file.startswith("."):
                filename = os.path.join(corpus, file)
                reviews_list.extend(read_csv(filename, limit))
        return reviews_list


if __name__ == '__main__':
    # Примеры использования
    l1 = read_corpus(CORPUS, limit=1)   # один отзыв из каждого направления
    l_all = read_corpus(CORPUS)    # читает весь корпус
    l_file = read_csv('new_corpus/Аптеки.csv')      # читает файл целиком
    l_file10 = read_csv('new_corpus/Аптеки.csv', 10)      # читает 10 отзывов из одного файла

    print(l1)
    print(l_file)
    print(l_file10)
