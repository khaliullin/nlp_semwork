import texterra
from nltk import word_tokenize

from parser import Parser


class Preprocessor:
    def __init__(self, X):
        self.X = X
        self.negative_words = ["не", "нет"]

    def preprocess(self):
        self.preprocessed_X = [self.preprocess_negative_parts(doc) for doc in self.X]

        return self.preprocessed_X

    def preprocess_negative_parts(self, doc):
        t = texterra.API('7c8f80b4a2cac05b4efd9d90d8f5f5f5f2534f88')

        self.tokens = self.tokenized_doc(doc)
        detected_syntax = t.syntax_detection(doc)

        for generator in detected_syntax:
            tree = generator.tree
            print(tree)
            for parent_tuple, children in tree.items():
                parent_word = parent_tuple[2]
                self.append_negative_gchildren_to_parents(parent_word, children)

        return self.tokens

    def append_negative_gchildren_to_parents(self, parent, children):
        for child in children:
            if not child:
                return

            for gchild, ggchild in child.items():
                gchild_word = gchild[2]
                if gchild_word in self.negative_words:
                   self.replace_token_with_negative(parent, gchild_word)

                self.append_negative_gchildren_to_parents(gchild_word, ggchild)


    def replace_token_with_negative(self, parent_token, negative):
        for i, token in enumerate(self.tokens):
            if token == parent_token:
                self.tokens[i] = negative + " " + token
                self.tokens.remove(negative)


    def tokenized_doc(self, doc):
        return word_tokenize(doc)

# test

if __name__ == '__main__':
    pr = Parser()
    docs = pr.read_csv('new_corpus/Аптеки.csv', 2)
    preprocessor = Preprocessor([docs[0]['text']])
    print(preprocessor.preprocess())