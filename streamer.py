import tweepy
import pandas as pd
from textblob import TextBlob
import mysql.connector
import re

import app
from app import db
#from db import storage
from config import Credentials, Settings



#Authentication
auth  = tweepy.OAuthHandler(Credentials.API_KEY, \
                            Credentials.API_SECRET_KEY)
auth.set_access_token(Credentials.ACCESS_TOKEN,  \
                      Credentials.ACCESS_TOKEN_SECRET)



#CREATE THE API OBJECT
api = tweepy.API(auth)

mydb = mysql.connector.connect(
    host="",
    user="root",
    passwd="",
    database="nlpmaster",
    charset = 'utf8'
)

if mydb.is_connected():
    mycursor = mydb.cursor()
    mycursor.execute(f'CREATE TABLE IF NOT EXISTS {Settings.TABLE_NAME} ({Settings.TABLE_ATTRIBUTES})')
    mydb.commit()

    mycursor.close()

    
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if status.retweeted:
        # Avoid retweeted info, and only original tweets will 
        # be received
            return True
        # Extract attributes from each tweet
        id_str = status.id_str
        created_at = status.created_at
        user_created_at = status.user.created_at
        text = deEmojify(status.text)    # Clean the emojis
        cleaned_text = clean_tweet(text)  #Preprocess the text with regex
        print('****'*10)
        print(status.text)
        print('\n\n')
        print('****'*10)
        print(cleaned_text)
        print('****'*10)
        #EXTRACT SOME EXTRA INFORMATION
        user_location = deEmojify(status.user.location)
        user_description = deEmojify(status.user.description)
        user_followers_count =status.user.followers_count

        

        #SENTIMENT ANALYSIS
        sentiment = TextBlob(text).sentiment
        polarity = sentiment.polarity
        subjectivity = sentiment.subjectivity

         
        longitude = None
        latitude = None
        
        if status.coordinates:
            longitude = status.coordinates['coordinates'][0]
            latitude = status.coordinates['coordinates'][1]

        retweet_count = status.retweet_count
        favorite_count = status.favorite_count
        
        #store data un mysql
        db.storage(id_str, created_at, cleaned_text, polarity, subjectivity, user_created_at, user_location, user_description, user_followers_count,longitude, latitude,\
                retweet_count, favorite_count)


    def on_error(self, status_code):
        '''
        Since Twitter API has rate limits, 
        stop srcraping data as it exceed to the threshold.
        '''
        if status_code == 420:
            # return False to disconnect the stream
            return False

#preprocessing text
def deEmojify(text):
    '''
    Strip all non-ASCII characters to remove emoji characters
    '''
    if text:
        return text.encode('ascii', 'ignore').decode('ascii')
    else:
        return None

def clean_tweet(tweet): 
    ''' 
    Use sumple regex statemnents to clean tweet text by removing links and special characters
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) \
                                |(\w+:\/\/\S+)", " ", tweet).split()) 



#CREATE THE STREAM LISTENER
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener = myStreamListener)
myStream.filter(languages=['en'], track = [Settings.TRACK_WORDS])

