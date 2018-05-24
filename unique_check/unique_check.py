import csv
import os


# class UniqueCheck():
#     def __init__(self, crawled_dir, test_dir):
#         self.crawled_dir = crawled_dir
#         self.test_dir = test_dir
#
#
# test_directory = "../corpus"
# crawled_directory = "../spr_crawler/corpus"
#
# check = UniqueCheck(crawled_directory, test_directory)
#
# check.print_stats()

def intersection(a, b):
    c = [value for value in a if value in b]
    return c

test_directory = "../corpus"

docs_sum = 0
test_directories_names = []

for index, dir in enumerate(os.walk(test_directory)):
    if index == 0:
        test_directories_names = dir[1]
        print("Количество тестовых папок: ", len(dir[1]))
    else:
        docs_sum += (len(dir[2]) - 2)  # 2 потому что есть линки и файл с названием папки)

print("Количество тестовых отзывов:", docs_sum)

crawled_directory = "../spr_crawler/corpus"

docs_sum = 0
crawled_directories_names = []

for index, dir in enumerate(os.walk(crawled_directory)):
    if index == 0:
        crawled_directories_names = dir[1]
        print("Количество скрауленых папок: ", len(dir[1]))
    else:
        docs_sum += (len(dir[2]) - 2)  # 2 потому что есть линки и файл с названием папки)

print("Количество скрауленых отзывов:", docs_sum)
same_as_test_directories_names = ["_".join(name.split(" ")) for name in crawled_directories_names]

intersection = intersection(test_directories_names, same_as_test_directories_names)

print("Количество пересекающихся названий папок: ",
      len(intersection))

test_folders = intersection

print(test_folders)

matched_sum = 0
crawled_sum = 0
test_sum = 0

# ЦИКЛ ПО ВСЕМ ПЕРЕСЕКШИМСЯ ПАПКАМ
for test_folder in test_folders:
    if not test_folder.startswith("."):
        test_reviews = os.listdir(os.path.join(test_directory, test_folder))[:-2]
        test_sum += len(test_reviews)

        crawled_folder = " ".join(test_folder.split("_"))

        crawled_reviews = os.listdir(os.path.join(crawled_directory, crawled_folder))
        crawled_sum += len(crawled_reviews)

        # ЦИКЛ ГДЕ ПРОБЕГАЕМСЯ ПРО СКРАУЛЕНЫМ ДОКАМ
        for crawled_review in crawled_reviews:
            print('\t' + crawled_review)

            crawled_review_path = os.path.join(crawled_directory, crawled_folder, crawled_review)
            crawled_reader = list(csv.reader(open(crawled_review_path, newline='\n'), delimiter='\n', quotechar='|'))
            crawled_title = crawled_reader[0][0]

            crawled_text = ' '.join(str(review) for paragraph in crawled_reader[1:] for review in paragraph)
            crawled_text = crawled_text[:-17]  # хардкод потому что в конце остается дата

            crawled_result = {"title": crawled_title, "text": crawled_text}

            # ЦИКЛ ГДЕ ПРОБЕГАЕМСЯ ПО ТЕСТОВЫМ ДОКАМ (ОТ ЕЛЕНЫ)
            for test_review in test_reviews:
                test_review_path = os.path.join(test_directory, test_folder, test_review)
                test_reader = list(csv.reader(open(test_review_path, newline='\n'), delimiter='\n'))
                test_title = test_reader[0][0]
                test_text = ' '.join(str(review) for paragraph in test_reader[1:] for review in paragraph)

                if test_text == crawled_text:
                    matched_sum += 1
                    break
                # А вот тут проверочка!!!

print("НОМЕР СОВПАВШИХ ДОКОВ:", matched_sum)
percent = float(matched_sum) / (test_sum - matched_sum + crawled_sum) * 100
print("ОБЪЕМ ТЕСТОВЫХ ОТЗЫВОВ", test_sum)
print("ОБЪЕМ СКРАУЛЕННЫХ ОТЗЫВОВ", crawled_sum)
print("ПРОЦЕНТ СОВПАДЕНИЯ!!!:::  ", percent, "%")




