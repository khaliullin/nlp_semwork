import csv
import glob
import os


def read_csv(filename):
    """
    Возвращает словарь {'title':, 'text':}
    """
    is_positive = filename[-5] == '1'
    reader = csv.reader(open(filename, newline='\n'), delimiter='\n')
    review_list = list(reader)
    review_dict = {'title': review_list[0][0],
                   'text': ' '.join(str(review) for paragraph in review_list[1:] for review in paragraph),
                   'positive': is_positive}
    return review_dict


def read_corpus(corpus, direction_name='', limit=-2):
    """
    :param corpus: Строка с названием папки корпуса
    :param direction_name: Конкретная папка с отзывами (прим. Больницы)
    :param limit: Количество читаемых файлов из корпуса
    :return: Пока ничего не возвращает
    """
    list_dicts = []
    if direction_name:
        folder = os.path.join(corpus, direction_name)
        for review in os.listdir(folder)[:limit]:
            list_dicts.append(read_csv(os.path.join(corpus, direction_name, review)))
    else:
        folder = os.listdir(corpus)
        for direction in folder:
            if not direction.startswith("."):
                for review in os.listdir(os.path.join(corpus, direction))[:limit]:
                    list_dicts.append(read_csv(os.path.join(corpus, direction, review)))
    return list_dicts


if __name__ == '__main__':
    corpus = 'corpus'
    l = read_corpus(corpus, direction_name='Аптеки', limit=40)
    print(l)
