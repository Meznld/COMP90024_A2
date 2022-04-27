import re
import string
import pandas as pd
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from emot.emo_unicode import UNICODE_EMO, EMOTICONS


from sklearn.feature_extraction.text import CountVectorizer

stop_words=stopwords.words('english')

def convert_emojis(text):
    for emot in UNICODE_EMO:
        text = text.replace(emot, "_".join(UNICODE_EMO[emot].replace(",","").replace(":","").split()))
    return text

def convert_emoticons(text):
    for emot in EMOTICONS:
        text = re.sub(u'('+emot+')', "_".join(EMOTICONS[emot].replace(",","").split()), text)
    return text

def preprosess_tweet(tweet):
    # remove urls
    tweet = re.sub(r"http\S+|www\S+|https\S+", '', tweet, flags=re.MULTILINE)

    # convert emojis and emoticon to words
    try:
        tweet = convert_emojis(tweet)
    except:
        tweet = tweet
    try: 
        tweet = convert_emoticons(tweet)
    except:
        tweet = tweet

    # remove hashtags and mentions
    tweet = re.sub(r'\@\w+|\#','', tweet)
    # remove multiple spaces
    tweet = re.sub("\s+"," ",tweet)
    # remove punctuations
    tweet = tweet.translate(str.maketrans('', '', string.punctuation))
    # convert to lower case
    tweet.lower()

    tweet_tokens = word_tokenize(tweet)
    result = [w for w in tweet_tokens if not w in stop_words]
    lemmatizer = WordNetLemmatizer()
    lemmawords = [lemmatizer.lemmatize(w) for w in result]
    return " ".join(lemmawords)

sentence = """At eight o'clock on Thursday morning
... Arthur didn't feel very good."""
