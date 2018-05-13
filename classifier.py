from lightgbm import LGBMClassifier
import numpy as np
from nltk import RegexpTokenizer
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline, FeatureUnion

from parser import Parser


class Classifier:

    def get_bayes_result(self, docs):
        return self.run_pipeline_with_clf(MultinomialNB(), docs)

    def get_svm_result(self, docs):
        return self.run_pipeline_with_clf(svm.SVC(), docs)

    def get_regression_result(self, docs):
        return self.run_pipeline_with_clf(LogisticRegression(), docs)

    def get_lgbm_result(self, docs):
        return self.run_pipeline_with_clf(LGBMClassifier(), docs)

    def run_pipeline_with_clf(self, clf, docs):
        twenty_train, twenty_test, target_train, target_test = train_test_split(docs['text'], docs['target'],
                                                                                test_size=0.3,
                                                                                random_state=1)
        text_clf = Pipeline([('vect', CountVectorizer()),
                             ('tfidf', TfidfTransformer()),
                             ('clf', clf),
                             ])
        text_clf.fit(twenty_train, target_train)

        predicted = text_clf.predict(twenty_test)
        return np.mean(predicted == target_test)

    def set_data(self, docs):
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
    data = classifier.set_data(docs)
    print("Logistic Regression", classifier.get_regression_result(data))
    print("SVM", classifier.get_svm_result(data))
    print("Naive Bayes", classifier.get_bayes_result(data))
    print("LGBMClassifier", classifier.get_lgbm_result(data))
