import nltk
from nltk.classify import ClassifierI

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