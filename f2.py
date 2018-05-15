import argparse

# Инициализируем аргументы командной строки
parser = argparse.ArgumentParser()
parser.add_argument('--lm', type=str, default="serialized_model",
                    help="Путь к сериализованной модели")
parser.add_argument('--src-test-texts', type=str, default="test_collection",
                    help="Путь к тестовой коллекции")
args = parser.parse_args()


# Вызываем функции для выполнения задачи

