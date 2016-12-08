from __future__ import division
#https://www.kaggle.com/kernels/diff/147679/148299
import string
from nltk.corpus import stopwords
import math
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from PorterStemmer import *

tokenize = lambda doc: doc.lower().split(" ")
def TokenStem(document):
    steemer=PorterStemmer()
    returner=[]
    document = document.lower().split(' ')
    for word in document:
        if(word not in stopwords.words('english')):
            word=re.sub('[^A-Za-z0-9]+', '', word)
            word=steemer.stem(word, 0, len(word) -1)
            returner.append(word)
    return returner



def term_frequency(term, tokenized_document):
    return tokenized_document.count(term)

def subTF(term, tokenized_document):
    count = tokenized_document.count(term)
    if count == 0:
        return 0
    return 1 + math.log(count)

def idfFunction(tokedDoc):
    idf_values = {}
    setOfTokens = set([item for sublist in tokedDoc for item in sublist])
    for tkn in setOfTokens:
        contains_token = map(lambda doc: tkn in doc, tokedDoc)
        idf_values[tkn] = 1 + math.log(len(tokedDoc)/(sum(contains_token)))
    return idf_values

def tfidf(documents):
    tokedDoc = [TokenStem(d) for d in documents]
    idf = idfFunction(tokedDoc)
    tfidf_documents = []
    for document in tokedDoc:
        doc_tfidf = []
        for term in idf.keys():
            tf = subTF(term, document)
            doc_tfidf.append(tf * idf[term])
        tfidf_documents.append(doc_tfidf)
    return tfidf_documents

def cosine_similarity(vector1, vector2):
    dot_product = sum(p*q for p,q in zip(vector1, vector2))
    magnitude = math.sqrt(sum([val**2 for val in vector1])) * math.sqrt(sum([val**2 for val in vector2]))
    if not magnitude:
        return 0
    return dot_product/magnitude
import httplib, urllib, base64
import json

def inNews(tweets):
    newsLister=lister()
    newsLister.append(tweets)
    newsVec=tfidf(newsLister)
    tweetVec=newsVec[-1]
    del newsVec[-1]
    for news in newsVec:
        num=cosine_similarity(news,tweetVec)
        print num
        if(num>0.25):
            return True
    return False


import unicodedata

def lister():
    newsList = []
    dict=newRequest()
    for lur in dict['value']:
        aa=unicodedata.normalize('NFKD', lur['description']).encode('ascii','ignore')
        newsList.append(aa)
    return newsList

def newRequest():
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'KEY',
    }

    params = urllib.urlencode({
        # Request parameters
        'Category': 'ScienceAndTechnology'
    })

    try:
        conn = httplib.HTTPSConnection('api.cognitive.microsoft.com')
        conn.request("GET", "/bing/v5.0/news/?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        d = json.loads(data)
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    return d
