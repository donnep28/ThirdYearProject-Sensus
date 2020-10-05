import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

stemming = PorterStemmer()

# Tokenizes the full_text and clears punctuation
class DataCleaning():

    def tokenize(df):
        #Gets each tweet
        tweet = df['full_text']
        tweet = str(tweet).lower()
        tokens = nltk.word_tokenize(tweet)
        token_words = [word for word in tokens if word.isalpha()] # Gets rid of punctuation and numbers
        return token_words

    # Stems words eg ['thanks' => 'thank']
    def stem_list(df):
        tweet = df['full_text']
        stemmed_list = [stemming.stem(word) for word in tweet]
        return (stemmed_list)

    # Removes stop words
    def remove_stopwords(df):
        tweet = df['full_text']
        cleaned_words = [word for word in tweet if word not in stop]
        return cleaned_words

    # Rejoins the list of words into cleaned tweet
    def rejoin(df):
        tweet = df['full_text']
        rejoined = (" ".join(tweet))
        return rejoined
