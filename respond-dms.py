# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 14:11:57 2022

@author: Saskia Hustinx
"""

import re
import gpt_2_simple as gpt2
import tensorflow as tf
import json
import tweepy
import random
import time

### NLP SECTION ###
def words_in_string(word_list, a_string):
    return set(word_list).intersection(a_string.split())

def generate_tweets(num):
    
    texts = gpt2.generate(sess, run_name='run2', temperature=0.9, length=50, nsamples=num, return_as_list=True)
    res = []
    
    for text in texts:
        match = re.findall('<|startoftext|>(.*?[\.\?!])', text)
        if len(match) == 3 and len(match[2]) > 40:
            if not words_in_string(filter_list, match[2]):
                res.append(match[2])
        
    return res


### TWITTER ###

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

def fetch_dms():
    # fetching the direct messages
    direct_messages = api.get_direct_messages()
      
    print(len(direct_messages))
    print(direct_messages)
    return direct_messages

def respond_dm(dms):
    recipients = []
    
    for dm in dms:
        if dm.message_create['sender_id'] != '1577695345865367553' and dm.message_create['sender_id'] not in recipients:
            recipients.append(dm.message_create['sender_id'])
        
    res_tweets = []

    while len(res_tweets) < len(recipients):
        res_tweets = generate_tweets(len(recipients) + 10)
        
    for recipient in recipients:
        api.send_direct_message(recipient_id = recipient, text = str("My message for you is: \n \n"+ random.choice(res_tweets) + " ✨"))
        
    time.sleep(5)


# main

api = api()
dms = fetch_dms()

if len(dms) > 0:
    tf.config.set_visible_devices([], 'GPU')
    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess, run_name='run2')

    # delete the outgoing dms
    dms = fetch_dms()
    for dm in dms:
        if dm.message_create['sender_id'] == '1577695345865367553':
            api.delete_direct_message(dm.id)
            dms.remove(dm)
    
    filter_list = ['victim', 'abuse', 'sex', 'planetary']
    respond_dm(dms)
    
    # delete reponded dms
    for dm in dms:
        api.delete_direct_message(dm.id)
        
    