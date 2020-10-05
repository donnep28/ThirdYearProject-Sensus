import tweepy
import json

class TwitterAPI:

    # Auth
    def auth(consumer_key, consumer_secret, access_key, access_secret):
        try:
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_key, access_secret)
            # Set to false if rate limited
            api = tweepy.API(auth)
        except tweepy.TweepError:
            api = False
        return api

    # Check valid user
    def is_valid_user(api, user):
        try:
            api.get_user(user)
            return True
        except tweepy.TweepError:
            return False

    # Get Tweets
    def get_reponse(api, user):
        response = tweepy.Cursor(api.search, q=user, exclude='retweets', tweet_mode="extended").items(10)
        return response

    # Extract Tweets
    def extract_tweets(response, user):
        result = []
        for tweets in response:
            tweets = {'created_at': tweets.created_at.strftime("%m-%d-%Y"),
                      'full_text': tweets.full_text,
                      'screen_name': tweets.user.screen_name, 
                      'user_mentioned': user}
            result.append(tweets)
        return result
