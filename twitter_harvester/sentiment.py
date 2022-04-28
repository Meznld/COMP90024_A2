import re
import string
import pandas as pd
import nltk
from nltk.corpus import stopwords

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from emot.emo_unicode import UNICODE_EMOJI



stop_words=stopwords.words('english')

def convert_emojis(text):
    for emot in UNICODE_EMOJI:
        text = text.replace(emot, "_".join(UNICODE_EMOJI[emot].replace(",","").replace(":","").split()))
    text = re.sub("_"," ",text)
    return text


def preprocess_tweet(tweet):
    # remove urls and links
    tweet = re.sub(r"http\S+|www\S+|https\S+|bit.ly/\S+'", '', tweet, flags=re.MULTILINE)
    tweet = tweet.strip('[link]')
    tweet = re.sub(r'pic.twitter\S+','', tweet)

    # remove retweet, hashtags and @user
    tweet = re.sub('(RT\s@[A-Za-z]+[A-Za-z0-9-_]+)', '', tweet) 
    tweet = re.sub('(@[A-Za-z]+[A-Za-z0-9-_]+)', '', tweet)
    tweet = re.sub('(#[A-Za-z]+[A-Za-z0-9-_]+)', '', tweet)

    # convert emojis and emoticon to words
    try:
        tweet = convert_emojis(tweet)
    except:
        tweet = tweet

    # remove multiple spaces
    tweet = re.sub("\s+"," ",tweet)
   
    # remove punctuations
    tweet = tweet.translate(str.maketrans('', '', string.punctuation))
    # convert to lower case
    

    tweet_tokens = word_tokenize(tweet)
    result = [w for w in tweet_tokens if not w in stop_words]
    lemmatizer = WordNetLemmatizer()
    lemmawords = [lemmatizer.lemmatize(w) for w in result]
    return " ".join(lemmawords)

sentence = """At eight o'clock on Thursday morning \n
... Arthur didn't feel very good. 😂 www.help.com"""
print(preprocess_tweet(sentence))