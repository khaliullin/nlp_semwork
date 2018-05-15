import argparse

# Инициализируем аргументы командной строки
parser = argparse.ArgumentParser()
parser.add_argument('--lm', type=str, default="serialized_model",
                    help="Путь к сериализованной модели")
parser.add_argument('--src-texts', type=str, default="texts",
                    help="Путь к коллекции")
parser.add_argument('--o-texts', type=str, default="output_f3.json",
                    help="Путь куда сохранить размеченную коллекцию")
args = parser.parse_args()


# Вызываем функции для выполнения задачи
