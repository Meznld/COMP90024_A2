import re
import string
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import couchdb


couch = couchdb.Server('http://admin:XlkLSNezrwOlQ0fIx5C6@172.26.128.201:30396/')
db = couch['augment']
test = []
for idx,val in enumerate(db):
    if idx < 20:

        test.append(db[val]['text'])

stop_words=stopwords.words('english')
sid = SentimentIntensityAnalyzer()

def polarity_score(compound):
   
    if compound == 0.0:
        return "neutral"
    elif compound < 0:
        return "negative"
    elif compound > 0:
        return "positive"

def preprocess_tweet(raw):
    # remove urls and links
    tweet = re.sub(r"http\S+|www\S+|https\S+|bit.ly/\S+'", '', raw, flags=re.MULTILINE)
    tweet = tweet.strip('[link]')
    tweet = re.sub(r'pic.twitter\S+','', tweet)

    # remove retweet, hashtags and @user
    tweet = re.sub(r"RT @[\w]*:", ' ', tweet, flags=re.MULTILINE)
    tweet = re.sub(r"#(\w+)", ' ', tweet, flags=re.MULTILINE)
    tweet = re.sub(r"@(\w+)", ' ', tweet, flags=re.MULTILINE)

    # remove multiple spaces
    tweet = re.sub("\s+"," ",tweet)

    scores = sid.polarity_scores(tweet)
    classify = polarity_score(scores['compound'])
    return print(tweet + "\n", scores, classify)




# sentence = """ 😩 At eight o'clock on Thursday morning \n
# ... Arthur didn't feel this very good.  www.help.com RT @aodsufh"""
# # print(preprocess_tweet(sentence))
# emoti = "i hate this"
# print(preprocess_tweet(sentence))
# # print(sentiment(preprocess_tweet(sentence)))

for i in test:

    preprocess_tweet(i)

