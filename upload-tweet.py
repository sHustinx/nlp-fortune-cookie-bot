# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 21:25:09 2022


- Authentication of bot-account via tweepy
- loading pre-trained checkpoint from disk
- generating and postprocessing tweets
- posting tweet

@author: Saskia Hustinx
"""
import re
import gpt_2_simple as gpt2
import tensorflow as tf
import json
import tweepy
import random

### TWITTER SECTION ###

# Parse the credentials for the twitter bot
with open("cred.json", "r") as json_file:
    twitter_creds = json.load(json_file)

# Set the credentials based on the credentials file
API_KEY = twitter_creds['api-key']
API_SECRET = twitter_creds['api-secret']
BEARER_TOKEN = twitter_creds['bearer-token']
ACCESS_KEY = twitter_creds['access-token']
ACCESS_SECRET = twitter_creds['access-secret']

def api():
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

    return tweepy.API(auth)

def tweet_message(api: tweepy.API, message: str):
    api.update_status(message)
    
### TWITTER SECTION END ###

### NLP SECTION ###

def words_in_string(word_list, a_string):
    return set(word_list).intersection(a_string.split())

tf.config.set_visible_devices([], 'GPU')
sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, run_name='run2')

filter_list = ['victim', 'abuse', 'sex', 'planetary', 'celestial']

def generate_tweets():
    
    texts = gpt2.generate(sess, run_name='run2', temperature=0.85, length=50, nsamples=10, return_as_list=True)
    res = []
    
    for text in texts:
        match = re.findall('<|startoftext|>(.*?[\.\?!])', text)
        if len(match) == 3 and 40 < len(match[2]) < 140:
            if not words_in_string(filter_list, match[2]):
                res.append(match[2])
        
    return res



res_tweets = []

while len(res_tweets) == 0:
    res_tweets = generate_tweets()


api = api()
tweet_message(api, random.choice(res_tweets))


    
