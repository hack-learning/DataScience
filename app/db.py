import mysql.connector
from config import Settings
import pandas as pd
import time
import datetime




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

def storage(id_str, created_at, text, polarity, subjectivity, user_created_at, user_location, user_description, user_followers_count,longitude, latitude,\
                retweet_count, favorite_count):
    if mydb.is_connected():
        mycursor = mydb.cursor()
        val = (id_str, created_at, text, polarity, subjectivity, user_created_at, user_location, \
              user_description, user_followers_count, longitude, latitude, retweet_count, favorite_count)
        sql = "INSERT INTO {} (id_str, created_at, text, polarity, subjectivity, user_created_at, user_location, user_description, user_followers_count, \
               longitude, latitude, retweet_count, favorite_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(Settings.TABLE_NAME)
        
        mycursor.execute(sql, val)
        mydb.commit()
        mycursor.close()

