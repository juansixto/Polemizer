#!/usr/bin/python
# -*- coding: utf-8 -*-

import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time


#Twitter information
CONSUMER_KEY = "YJ3J6hB9OtZ6J2OwVPeFJw"
CONSUMER_SECRET="EhrZSHIM6MedoBdckw3k60k5Fs4DgkOmcMbCcgDnMw"
ACCESS_KEY="1857555254-EeLmhfGjpOW7bVowVJIX4OFEta7RhuAASjK73RD"
ACCESS_SECRET="k0LJnjERampLlPn6kYwIJMzhqZ7Rg1MZ46IWVDPvdI"
LAST_ID="381051711944916992"
TRENDS = []
TWEETS = []
RESPONSE_TWEETS = []
RESPONSE_USERS = []


class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_data(self, data):
        print data['trends']
        return True

    def on_error(self, status):
        print status

def openLog():
    infile = open('TweetLog.txt', 'r')
    print('>>> Lectura completa del TweetLog')
    for line in infile:
        print(line)
        RESPONSE_TWEETS.append(line)
    # Cerramos el fichero.
    infile.close()
    infile = open('UsersLog.txt', 'r')
    print('>>> Lectura completa del UsersLog')
    for line in infile:
        print(line)
        RESPONSE_USERS.append(line)
    # Cerramos el fichero.
    infile.close()

def writeLog():
    outfile = open('TweetLog.txt', 'w') # Indicamos el valor 'w'.
    for tweet in RESPONSE_TWEETS:
        outfile.write(tweet)
    outfile.close()
    outfile = open('UsersLog.txt', 'w') # Indicamos el valor 'w'.
    for user in RESPONSE_USERS:
        outfile.write(user)
    outfile.close()

def start_data():
    global API, TRENDS, TWEETS
    TRENDS = []
    l = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    API = tweepy.API(auth)
    print API.me().name
    #API.update_status('')
    me = API.me()
    print me.followers_count
    print me.status.text
    print me.statuses_count
    print me.location
    for i in API.trends_place('23424950'):
        for t in i['trends']:
            TRENDS.append(t['name'])
            
            
def buscar_movida():
    global API, TRENDS, TWEETS
    TWEETS = []
    movida = False
    LAST_ID="0"
    while(movida == False):
        tweets = API.home_timeline()
        LAST_ID= tweets[0].id
        temas_interesantes(tweets)
        for t in tweets:
            TWEETS.append(t)
        writeLog()
        time.sleep(60)
        
def temas_interesantes(tweets):
    global RESPONSE_TWEETS
    for t in TRENDS:
        for tw in TWEETS:
            if tw.text.find(t) >= 0:
                print "Encontrado " + t + " en " + tw.text
                print "por " + tw.user.screen_name
                if (not tw.id in RESPONSE_TWEETS) and (not tw.user.screen_name in RESPONSE_USERS):
                    API.update_status( "@"+ tw.author.screen_name + " No parais de sacar mierda sobre el asunto de "+t+" ¿Contentos?" , tw.id)
                    RESPONSE_TWEETS.append(tw.id)
    
if __name__ == '__main__':
    openLog()
    start_data()
    buscar_movida()

