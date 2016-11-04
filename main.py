import unirest
import requests, urllib, pprint
tweet="it is terrible, horrible, and very bad"
url='https://jamiembrown-tweet-sentiment-analysis.p.mashape.com/api/?text='+tweet
response = unirest.get(url,
  headers={
    "X-Mashape-Key": "Key",
    "Accept": "application/json"
  }
)
tweetScore=response.body['score']
tweetSentiment=response.body['sentiment']
print tweetScore
print tweetSentiment
