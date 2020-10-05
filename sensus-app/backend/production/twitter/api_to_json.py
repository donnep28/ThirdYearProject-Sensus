import sys
import json
import pandas as pd
import tempfile

import pandas as pd
import boto3
import base64
from botocore.exceptions import ClientError

from twitter import TwitterAPI
from secrets import Secrets

from __future__ import print_function

#sys.path.append('../')

def lambda_handler(event, context):
    
    for record in event['Records']:
        twitter_handle = record['dynamodb']['NewImage']['message']['M']['username']['S']
        destination_bucket_name = 'sensus-tweets-raw'
        
        print("Twitter handle:", twitter_handle)
        print("Destination Bucket:", destination_bucket_name)


        # Instantiate Class, retrieve Twitter credentials
        s = Secrets()

        twitter_secret_name = 'prod/sensus/twitter_api'
        region_name = 'eu-west-1'

        twitter_credentials = s.get_secret(twitter_secret_name, region_name)

        consumer_key = twitter_credentials['consumer_key']
        consumer_secret = twitter_credentials['consumer_secret']
        access_key = twitter_credentials['access_key']
        access_secret = twitter_credentials['access_secret']

        # Set AWS credentials
        session = boto3.Session(
            aws_access_key_id='AKIA6DC3AMH273FBFDNW',
            aws_secret_access_key='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',
            region_name='eu-west-1'
        )

        # Create S3 connection
        s3 = session.resource('s3')

        #twitter_handle = 'realDonaldTrump'
        api = TwitterAPI.auth(consumer_key, consumer_secret, access_key, access_secret)

        # Write tweets to 'raw' data lake
        if TwitterAPI.is_valid_user(api, twitter_handle):
            response = TwitterAPI.get_reponse(api, twitter_handle)
            result = TwitterAPI.extract_tweets(response, twitter_handle)

            df = pd.DataFrame(result)
            destination_key_name = 'tweets/date={}/twitter_handle={}/data.json'.format(df['created_at'][0], df['user_mentioned'][0])
            with tempfile.NamedTemporaryFile(mode='w') as f:
                df.to_json(f.name)
                s3.Bucket('sensus-raw-tweets') \
                    .upload_file(f.name, destination_key_name)