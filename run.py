from __future__ import division
from Finance import *
import main
import re
import processing
import sched, time
s = sched.scheduler(time.time, time.sleep)
def call(sc,text,priceDict):
    price=float(priceDict['price'])
    open=float(priceDict['open'])
    PriceChange=price-open
    PricePercentage=open/abs(PriceChange)*100
    priceEffected=False
    positivePrice=False
    if(PricePercentage>=3):
        priceEffected=True
    else:
        priceEffected=False
    negativeInfluence=0
    negList=[]
    positiveInfluence=0
    posList=[]
    tweetDict=main.request(text)
    for item in tweetDict['neg']:
        negativeInfluence+=item[1]
        #print item
    for item in tweetDict['pos']:
        #print item
        positiveInfluence+=item[1]
    if(len(posList)!=0):
        if(positiveInfluence*3>=posList[-1]):
            tweetList=[]
            for item in tweetDict['pos']:
                textOfTweet=item['text']
                re.sub("/n", '', textOfTweet)
                textOfTweet = re.sub('[^a-zA-Z0-9 ]', '', textOfTweet)
                listOfWord=textOfTweet.split(' ')
                for word in listOfWord:
                    tweetList=tweetList+' '+word
            if(processing.inNews(tweetList)==False):
                if(priceEffected==False):
                    print 'BUY'
    if (len(negList) != 0):
        if (negativeInfluence * 3 >= negList[-1]):
            tweetList = []
            for item in tweetDict['neg']:
                textOfTweet = item['text']
                re.sub("/n", '', textOfTweet)
                textOfTweet = re.sub('[^a-zA-Z0-9 ]', '', textOfTweet)
                listOfWord = textOfTweet.split(' ')
                for word in listOfWord:
                    tweetList = tweetList + ' ' + word
            if (processing.inNews(tweetList) == False):
                if(priceEffected==False):
                    print 'SELL'
    s.enter(10, 1, call, (sc, text,priceDict,))
companyName = raw_input('Enter Company Name: ')
text=raw_input("Enter keywords: ")
text=text.replace(' ',' or ')
priceDict=price(companyName)
# s.enter(60, 1, request(requestString), (s,))
# t=Timer(60.0, request(requestString))
# t.start()
#show()
s.enter(1, 1, call, (s, text, priceDict,))
s.run()
#call(text,priceDict)
