import random
import pickle
from statistics import mode

import pandas as pd
import numpy as np
import nltk

from nltk.classify.scikitlearn import SklearnClassifier
from nltk.classify import ClassifierI

from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC, NuSVC


documents_f = open("pickled_algos/documents.pickle", "rb")
documents = pickle.load(documents_f)
documents_f.close()

word_features_f = open("pickled_algos/word_features.pickle", "rb")
word_features = pickle.load(word_features_f)
word_features_f.close()

feature_sets_f = open("pickled_algos/feature_sets.pickle", "rb")
feature_sets = pickle.load(feature_sets_f)
feature_sets_f.close()


random.shuffle(feature_sets)

training_set = feature_sets[:10000]
testing_set = feature_sets[10000:]

def find_features(document):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features

Implement Voting System
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


# Load our Pickles 🥒

# BasicNB
open_file = open("pickled_algos/basic_nb.pickle", "rb")
BasicNB_classifier = pickle.load(open_file)
open_file.close

# MNB
open_file = open("pickled_algos/mnb.pickle", "rb")
MNB_classifier = pickle.load(open_file)
open_file.close

# BernoulliNB
open_file = open("pickled_algos/bernoulli.pickle", "rb")
BernoulliNB_classifier = pickle.load(open_file)
open_file.close

# LogisticRegression
open_file = open("pickled_algos/logistic.pickle", "rb")
LogisticRegression_classifier = pickle.load(open_file)
open_file.close

# SVC
open_file = open("pickled_algos/svc.pickle", "rb")
SVC_classifier = pickle.load(open_file)
open_file.close

# LinearSVC
open_file = open("pickled_algos/linear.pickle", "rb")
LinearSVC_classifier = pickle.load(open_file)
open_file.close

# NuSVC
open_file = open("pickled_algos/nu.pickle", "rb")
NuSVC_classifier = pickle.load(open_file)
open_file.close

# Vote for the most accurate classifier
voted_classifier = VoteClassifer(
    BasicNB_classifier,
    MNB_classifier,
    BernoulliNB_classifier,
    LogisticRegression_classifier,
    SVC_classifier,
    LinearSVC_classifier,
    NuSVC_classifier
)


def sentiment(text):
    feats = find_features(text)
    # Return the classification and the confidence level
    return voted_classifier.classify(feats), voted_classifier.confidence(feats)

