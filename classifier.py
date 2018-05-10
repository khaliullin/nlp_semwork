import lightgbm as lgb
import numpy as np
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from parser import Parser


class Classifier:

    @staticmethod
    def get_bayes_result(docs):
        twenty_train, twenty_test, target_train, target_test = train_test_split(docs['text'], docs['target'],
                                                                                test_size=0.2,
                                                                                random_state=len(docs))
        text_clf = Pipeline([('vect', CountVectorizer()),
                             ('tfidf', TfidfTransformer()),
                             ('clf', MultinomialNB()),
                             ])
        text_clf.fit(twenty_train, target_train)

        predicted = text_clf.predict(twenty_test)
        return np.mean(predicted == target_test)

    @staticmethod
    def get_svm_result(docs):
        twenty_train, twenty_test, target_train, target_test = train_test_split(docs['text'], docs['target'],
                                                                                test_size=0.2,
                                                                                random_state=1)
        text_clf = Pipeline([('vect', CountVectorizer()),
                             ('tfidf', TfidfTransformer()),
                             ('clf', svm.SVC()),
                             ])
        text_clf.fit(twenty_train, target_train)

        predicted = text_clf.predict(twenty_test)
        return np.mean(predicted == target_test)

    @staticmethod
    def get_regression_result(docs):
        twenty_train, twenty_test, target_train, target_test = train_test_split(docs['text'], docs['target'],
                                                                                test_size=0.2,
                                                                                random_state=len(docs))
        text_clf = Pipeline([('vect', CountVectorizer()),
                             ('tfidf', TfidfTransformer()),
                             ('clf', LogisticRegression()),
                             ])
        text_clf.fit(twenty_train, target_train)

        predicted = text_clf.predict(twenty_test)
        return np.mean(predicted == target_test)

    @staticmethod
    def get_lgbm_result(docs):
        twenty_train, twenty_test, target_train, target_test = train_test_split(docs['text'], docs['target'],
                                                                                test_size=0.2,
                                                                                random_state=len(docs))
        text_clf = Pipeline([('vect', CountVectorizer()),
                             ('tfidf', TfidfTransformer()),
                             ('clf', lgb.sklearn.LGBMClassifier()),
                             ])
        text_clf.fit(twenty_train, target_train)

        predicted = text_clf.predict(twenty_test)
        return np.mean(predicted == target_test)

    @staticmethod
    def get_data(docs):
        result = dict()
        text = []
        target = []
        for doc in docs:
            text.append(doc['text'])
            target.append(doc['positive'])
        result['text'] = text
        result['target'] = target
        return result


if __name__ == '__main__':
    pr = Parser()
    classifier = Classifier()
    docs = pr.read_csv('new_corpus/Аптеки.csv', 1000)
    data = classifier.get_data(docs)
    print("Logistic Regression", classifier.get_regression_result(data))
    print("SVM", classifier.get_svm_result(data))
    print("Naive Bayes", classifier.get_bayes_result(data))
    print("LGBMClassifier", classifier.get_lgbm_result(data))
