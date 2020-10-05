import random
import pickle
from statistics import mode

import pandas as pd
import numpy as np
import nltk

from nltk.classify.scikitlearn import SklearnClassifier
from nltk.tokenize import word_tokenize
from nltk.classify import ClassifierI

from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC, NuSVC

from voting import VoteClassifer


# Implement Voting System
class VoteClassifer(ClassifierI):
    # * = variable number of arguments
    def __init__(self, *classifiers):
        self._classifiers = classifiers
 
    def classify(self, features):
        votes = []
        # Iterate over each classifer
        for c in self._classifiers:
            # Get the vote for each classifer
            v = c.classify(features)
            votes.append(v)
        # Choose who got the most votes
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        
        # Count occurences of the most popular votes
        choice_votes = votes.count(mode(votes))
        # conf = occurence of most popular vote / len(votes)
        conf = float(choice_votes) / len(votes)

        return conf


def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features


# Import training sentiment140 training data
short_positive = open("140_pos.txt").read()
short_negative = open("140_neg.txt").read()

documents = []

for r in short_positive.split('\n'):
    documents.append(( r, "pos"))

for r in short_negative.split('\n'):
    documents.append(( r, "neg"))

all_words = []

# Tokenizew training daata
short_positive_words = word_tokenize(short_positive)
short_negative_words = word_tokenize(short_negative)

for w in short_positive_words:
    all_words.append(w.lower())

for w in short_negative_words:
    all_words.append(w.lower())

all_words = nltk.FreqDist(all_words)

# Create word features
word_features = list(all_words.keys())[:5000]


feature_sets = [(find_features(rev), cat) for (rev, cat) in documents]
print('1. feature_sets')


# Shuffle to randomise training data
random.shuffle(feature_sets)

# Create training and testing sets
training_set = feature_sets[:19000]
testing_set = feature_sets[19000:]

print('2. Pickled training_set, testing_set')

# Pickle documents, word_features, feature_sets
save_documents = open("pickled_algos/documents.pickle", "wb")
pickle.dump(documents, save_documents)
save_documents.close()

save_word_features = open("pickled_algos/word_features.pickle", "wb")
pickle.dump(word_features, save_word_features)
save_word_features.close()

save_feature_sets = open("pickled_algos/feature_sets.pickle", "wb")
pickle.dump(feature_sets, save_feature_sets)
save_feature_sets.close()

print('3. Pickled documents, word_features, feature_sets')

# BasicNB
BasicNB = nltk.NaiveBayesClassifier.train(training_set)
print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(BasicNB, testing_set))*100)

save_classifer = open("pickled_algos/basic_nb.pickle", "wb")
pickle.dump(BasicNB, save_classifer)
save_classifer.close()

# MNB
MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set))*100)

save_classifer = open("pickled_algos/mnb.pickle", "wb")
pickle.dump(MNB_classifier, save_classifer)
save_classifer.close()

# BernoulliNB
BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(training_set)
print("BernoulliNB_classifier accuracy percent:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set))*100)

save_classifer = open("pickled_algos/bernoulli.pickle", "wb")
pickle.dump(BernoulliNB_classifier, save_classifer)
save_classifer.close()

# LogisticRegression
LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print("LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)

save_classifer = open("pickled_algos/logistic.pickle", "wb")
pickle.dump(LogisticRegression_classifier, save_classifer)
save_classifer.close()

# SVC
SVC_classifier = SklearnClassifier(SVC())
SVC_classifier.train(training_set)
print("SVC_classifier accuracy percent:", (nltk.classify.accuracy(SVC_classifier, testing_set))*100)

save_classifer = open("pickled_algos/svc.pickle", "wb")
pickle.dump(SVC_classifier, save_classifer)
save_classifer.close()

# LinearSVC
LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)

save_classifer = open("pickled_algos/linear.pickle", "wb")
pickle.dump(LinearSVC_classifier, save_classifer)
save_classifer.close()

# NuSVC
NuSVC_classifier = SklearnClassifier(NuSVC())
NuSVC_classifier.train(training_set)
print("NuSVC_classifier accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, testing_set))*100)

save_classifer = open("pickled_algos/nu.pickle", "wb")
pickle.dump(NuSVC_classifier, save_classifer)
save_classifer.close()

print('Training complete 💯')


# Create Vote Classifier
voted_classifier = VoteClassifer(
   BasicNB,
   MNB_classifier,
   BernoulliNB_classifier,
   LogisticRegression_classifier,
   SVC_classifier,
   LinearSVC_classifier,
   NuSVC_classifier
)
