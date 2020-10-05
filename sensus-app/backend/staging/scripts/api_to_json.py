from __future__ import print_function

import sys
import json
import pandas as pd
import tempfile
import os

import pandas as pd
import boto3
import base64
from botocore.exceptions import ClientError

from twitter import TwitterAPI
from prepping import DataCleaning

def lambda_handler(event, context):
    
    # Read from DynamoDB records
    for record in event['Records']:
        twitter_handle = record['dynamodb']['NewImage']['message']['M']['username']['S']

        # Retrieve Twitter API, stored in Lambdas environment variables
        consumer_key = os.environ['consumer_key']
        consumer_secret = os.environ['consumer_secret']
        access_key = os.environ['access_key']
        access_secret = os.environ['access_secret']
        
        s3_resource = boto3.resource('s3')
        destination_bucket_name = 'sensus-tweets-raw'
        
        
        tmp = tempfile.NamedTemporaryFile()
        api = TwitterAPI.auth(consumer_key, consumer_secret, access_key, access_secret)
        
        if not api:
            consumer_key = os.environ['consumer_key_1']
            consumer_secret = os.environ['consumer_secret_1']
            access_key = os.environ['access_key_1']
            access_secret = os.environ['access_secret_1']
            api = TwitterAPI.auth(consumer_key, consumer_secret, access_key, access_secret)

        twitter_handle = twitter_handle.lower()
        if not TwitterAPI.is_valid_user(api, twitter_handle):
            response = {
                status: 400,
                errors: [
                    {
                        code: '400',
                        message: 'Ivalid User'
                    }
                ]
            }
            context.fail(json.stringify(resonse))

        else:
            response = TwitterAPI.get_reponse(api, twitter_handle)
            
            result = TwitterAPI.extract_tweets(response, twitter_handle)
            df = pd.DataFrame(result)
            
            # Clean the data before writing
            df['full_text'] = df.apply(DataCleaning.tokenize, axis=1)
            df['full_text'] = df.apply(DataCleaning.stem_list, axis=1)
            df['full_text'] = df.apply(DataCleaning.remove_stopwords, axis=1)
            df['full_text'] = df.apply(DataCleaning.rejoin, axis=1)

            # Open the file for writing
            df.to_json(tmp.name, orient='records', lines=True)

            # Upload to S3
            key = 'tweets/date={}/user={}/data.json'.format(df['created_at'][0], df['user_mentioned'][0])
            s3_resource.Bucket('sensus-raw-tweets').upload_file(tmp.name, key)
    