import argparse

# Инициализируем аргументы командной строки
parser = argparse.ArgumentParser()
parser.add_argument('--src-train-texts', type=str, default="/new_corpus", required=False,
                    help="Путь к корпусу, обязательный аргумент")
parser.add_argument('--text-encoding', type=str, default='UTF-8', help="Кодировка текста в файлах корпуса")
parser.add_argument('--word-type', choices=["surface_all", "surface_no_pm", "stem", "suffix_X"],
                    default="surface_no_pm",
                    help="В случае surface_all в качестве слов берутся все токены как есть.\n"
                         "В случае surface_no_pm – все токены, кроме знаков пунктуаций.\n"
                         "В случае stem – стемма.\n"
                         "В случае suffix_X – окончания слов длиной X")
parser.add_argument('-n', type=int, default=1, help="N-грамность. Слова, словосочетания и т.д.", required=False, )
parser.add_argument('--features', choices=['true', 'false'], default="false",
                    help="Использовать дополнительные hand-crafted признаки, указанные в задании")
parser.add_argument('--laplace', '-l', action='store_true', help="Использовать сглаживание по Лапласу")
parser.add_argument('--unknown-word-freq', type=int, default="1",
                    help="Частота, ниже которой слова в обучающем множестве считаются неизвестными")
parser.add_argument('-o', required=False, type=str, default="f1_output",
                    help="Путь куда сохранить сериализованную языковую модель")
args = parser.parse_args()


# Вызываем функции для выполнения задачи

