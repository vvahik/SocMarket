from __future__ import division
from threading import Timer
import unirest
import oauth2
import json
import re
from urllib2 import URLError
#from pylab import *
import requests, urllib, pprint
# url='https://jamiembrown-tweet-sentiment-analysis.p.mashape.com/api/?text='+tweet
# response = unirest.get(url,
#   headers={
#     "X-Mashape-Key": "KEY HIDDEN",
#     "Accept": "application/json"
#   })
# tweetScore=response.body['score']
# tweetSentiment=response.body['sentiment']
# print tweetScore
# print tweetSentiment
positiveTweets=[]
negativeTweets=[]

def oauth_req(url, key, secret, http_method="GET", post_body='', http_headers=None):
    consumer = oauth2.Consumer(key='KEY', secret='SEC')
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
    return content
headers={
                                   "X-Mashape-Key": "KEY",
                                   "Accept": "application/json" }
requestString='Apple'

def request(sting):
    AllTweets={}
    PernegInfluence = 0
    PerposInfluence = 0
    negInfluence = 0
    posInfluence = 0
    home_timeline = oauth_req( 'https://api.twitter.com/1.1/search/tweets.json?q='+ sting+'&result_type=recent', 'KEY', 'SEC' )
    d = json.loads(home_timeline)
    count=1
    negCount=0
    posCount=0
    PernegInfluence=negInfluence
    AllTweets['pos']=[]
    AllTweets['neg']=[]
    negInfluence=0
    posInfluence=0
    for stat in d['statuses']:
        listToAppend=[]
        tweet= stat['text'].encode('utf8')
        tweetRet=stat['retweet_count']
        tweetFav=stat['favorite_count']
        tweetUser=stat['user']['screen_name']
        userRequest = oauth_req('https://api.twitter.com/1.1/users/lookup.json?screen_name='+ tweetUser,
                        'KEY',
                        'SEC')
        user=json.loads(userRequest)
        re.sub("/n",' ',tweet)
        tweet = re.sub('[^a-zA-Z0-9]', ' ', tweet)
        if(stat['lang']!='en'):
            continue
        try:
            url = 'https://jamiembrown-tweet-sentiment-analysis.p.mashape.com/api/?text=' + str(tweet)
            response = unirest.get(url, headers=headers)
                                   # headers={
                                   #     "X-Mashape-Key": "BUkeL7hxhGmshsISnWOul7G3y4G0p136jT7jsnytrVZ9PmVTBd",
                                   #     "Accept": "application/json"
                                   # })
        except URLError,e:
            continue

        if(len(response.body)==3):
            tweetScore = response.body['score']
            tweetSentiment = response.body['sentiment']
            if(tweetSentiment=='negative'):
                negInfluence=tweetRet*5+tweetFav*2 + 1.5*user[0]['followers_count']
                listToAppend.append(stat)
                listToAppend.append(negInfluence)
                AllTweets['neg'].append(listToAppend)
                negativeTweets.append(stat['text'])
            elif(tweetSentiment=='positive'):
                posInfluence=tweetRet*5+tweetFav*2 + 1.5*user[0]['followers_count']
                listToAppend.append(stat)
                listToAppend.append(posInfluence)
                AllTweets['pos'].append(listToAppend)
                positiveTweets.append(stat['text'])
            else:
                continue
    return AllTweets

#     s.enter(60, 1, request(requestString), (s,))
# # t=Timer(60.0, request(requestString))
# # t.start()
# import sched, time
# s = sched.scheduler(time.time, time.sleep)
#
# s.enter(60, 1, request(requestString), (s,))
# s.run()
#show()
