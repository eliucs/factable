'''
    analysis.py

    Reads from .pickle files from the already
    trained classifiers to build the Vote Classifier.
'''


import pickle
from nltk import word_tokenize, sent_tokenize
from nltk.classify import ClassifierI
from statistics import mode


class VoteClassifier(ClassifierI):

    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        return mode(votes)


documentsFile = open('factcheck/saved_documents.pickle', 'rb')
documents = pickle.load(documentsFile)
documentsFile.close()

wordFeaturesFile = open('factcheck/saved_word_features.pickle', 'rb')
wordFeatures = pickle.load(wordFeaturesFile)
wordFeaturesFile.close()

featureSetsFile = open('factcheck/saved_feature_set.pickle', "rb")
featureSets = pickle.load(featureSetsFile)
featureSetsFile.close()

# Training and testing set
open_file = open('factcheck/trainedClassifiers/mnb.pickle', 'rb')
MultinomialNBClassifier = pickle.load(open_file)
open_file.close()

open_file = open('factcheck/trainedClassifiers/bnb.pickle', 'rb')
BernoulliNBClassifier = pickle.load(open_file)
open_file.close()

open_file = open('factcheck/trainedClassifiers/lreg.pickle', 'rb')
LogisticRegressionClassifier = pickle.load(open_file)
open_file.close()

open_file = open('factcheck/trainedClassifiers/lsvc.pickle', 'rb')
LinearSVCClassifier = pickle.load(open_file)
open_file.close()

open_file = open('factcheck/trainedClassifiers/sgd.pickle', 'rb')
StochasticGradientDescentClassifier = pickle.load(open_file)
open_file.close()

voteClassifier = VoteClassifier(MultinomialNBClassifier,
                                BernoulliNBClassifier,
                                LogisticRegressionClassifier,
                                StochasticGradientDescentClassifier,
                                LinearSVCClassifier)


def findFeatures(document):
    words = word_tokenize(document)
    features = {}
    for w in wordFeatures:
        features[w] = (w in words)

    return features


def factAnalysis(text):
    text = sent_tokenize(text)
    trueCount = 0
    falseCount = 0

    sentenceLabels = []
    for sentence in text:
        features = findFeatures(sentence)
        if voteClassifier.classify(features):
            trueCount += 1
            sentenceLabels.append((sentence, True))
        else:
            falseCount += 1
            sentenceLabels.append((sentence, False))

    print(trueCount)
    print(falseCount)
    print(sentenceLabels)

    if not sentenceLabels:
        return False, False, False
    elif trueCount > falseCount:
        return True, 1 - falseCount/trueCount, sentenceLabels
    else:
        return False, 1 - trueCount/falseCount, sentenceLabels