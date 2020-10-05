import tweepy
import json

class TwitterAPI:

    # Auth
    def auth(consumer_key, consumer_secret, access_key, access_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        return api

    # Check User
    def is_valid_user(api, user):
        try:
            api.get_user(user)
            return True
        except tweepy.TweepError:
            print('Not a valid User')

    # Get Tweets
    def get_reponse(api, user):
        response = tweepy.Cursor(api.search, q=user, exclude='retweets', tweet_mode="extended").items(100)
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
