import random
import pickle
import time
import tempfile
import logging

import pandas as pd
import numpy as np
import boto3
import requests

from twitter import TwitterAPI
from voting import VoteClassifer
from classification import Classification

start = time.time()

# Create to S3, DynamoDB
s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('prod_metrics')

consumer_key = 'k13L43yEGjpc5ayn82AE8EcVv'
consumer_secret = 'jmdIFl4lYVgZp94MAm9KSzEHUf1zV7vLB3bdmepiKKOIk72l59'
access_key = '942386900467355648-jFK98tzyZvI4HCxReB3itgi0xQOp1a4'
access_secret = 'iVdm1MtaPYfJE8UkIHQFGdwmAKnyRnr0Nevy5w4BEYIf1'

user = 'dominos' 
api = TwitterAPI.auth(consumer_key, consumer_secret, access_key, access_secret)

if TwitterAPI.is_valid_user(api, user):
    response = TwitterAPI.get_reponse(api, user)
    result = TwitterAPI.extract_tweets(response, user)
    
    tweets_df = pd.DataFrame(result)

end1 = time.time()
logging.info('Loaded Tweets', end1 - start)

# Load documents, word_features and feature_sets
documents = pickle.loads(s3.Bucket("sensus-pickled-algorithms").Object("nb/documents.pickle").get()['Body'].read())
word_features = pickle.loads(s3.Bucket("sensus-pickled-algorithms").Object("nb/word_features.pickle").get()['Body'].read())
feature_sets = pickle.loads(s3.Bucket("sensus-pickled-algorithms").Object("nb/feature_sets.pickle").get()['Body'].read())

# Load pickled 🥒 algorithms: BasicNB, BernoulliNB, MNB
BasicNB_classifier = pickle.loads(s3.Bucket("sensus-pickled-algorithms").Object("nb/basic_nb.pickle").get()['Body'].read())
BernoulliNB_classifier = pickle.loads(s3.Bucket("sensus-pickled-algorithms").Object("nb/bernoulli.pickle").get()['Body'].read())
MNB_classifier = pickle.loads(s3.Bucket("sensus-pickled-algorithms").Object("nb/mnb.pickle").get()['Body'].read())

end2 = time.time()
logging.info("Loaded Algo's", end2 - start)

# Vote for the most accurate classifier
voted_classifier = VoteClassifer(
    BasicNB_classifier,
    BernoulliNB_classifier,
    MNB_classifier
)

# Features
def find_features(document):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features

# Sentiment
def sentiment(text):
    feats = find_features(text)
    return voted_classifier.classify(feats)

# Count
def count_pos_neg(df):
    tot = len(df.index)
    pos = df['sentiment'].str.count("pos").sum() / tot * 100
    neg = df['sentiment'].str.count("neg").sum() / tot * 100
    res = {
        "positive": str(pos), 
        "negative": str(neg)
    }
    return res

# Ratio of Pos to Neg
def pos_neg_ratio(df):
    pos = df['sentiment'].str.count("pos").sum()
    neg = df['sentiment'].str.count("neg").sum()
    r1 = pos // neg
    r2 = neg // pos
    if r1 > r2:
        return str(r1) + ":1"
    return "1:" + str(r2)
    return "%s" % float((pos/r) / (pos/r))

end3 = time.time()
logging.info('Started Classification...', end3 - start)

# Apply Classification
tweets_df['sentiment'] = tweets_df['full_text'].apply(c.sentiment)

end4 = time.time()
logging.info('Completed Classification...', end4 - start)

# Apply Count, Ratio
sentiment_scores = count_pos_neg(tweets_df)
sentiment_ratio = pos_neg_ratio(tweets_df)

# Extract Keywords
res_series =  pd.Series(' '.join(tweets_df['full_text']).lower().split()).value_counts()[:5]
top_keywords = res_series.to_dict()

# Extract Hashtags
res_series = tweets_df.full_text.str.extractall(r'(\#\w+)')[0].value_counts()
top_hashtags = res_series.to_dict()

# Write results to production database (prod_metrics)
response = table.put_item(
   Item={
        'user': user,
        'top_keywords': top_keywords,
        'top_hastags': top_hashtags,
        'sentiment_ratio': sentiment_ratio,
        'sentiment_scores': sentiment_scores
   }
)