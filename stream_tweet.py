
import tweepy
from tweepy.auth import OAuthHandler
from tweepy import Stream
import json
import os
import matplotlib.pyplot as plt
import geopandas as gpd
import fiona
import pandas as pd


api_key = 'RF78G9kS9YenS6eB6GEwcXg4o'
api_secret_key = '7yl0aW8s4Mg5dZgCMMamlTQ1SIN40frPlpin6Vnwb0TZGvRRnp'
access_token = '1343516103222251522-ITVMH6zGvtjmfSOGlGeN7j7JY9wATM'
access_token_secret = 'whImRAgACzng0PT4OyU6lb90KIxbU4V0YxxxGUpcGko5s'
fp = '/Users/belkok/Documents/GitHub/COMP90024/COMP90024_A2/data/metro_suburbs_shape/metro_suburbs.shp'

def get_region(file_path):
    read_fp = gpd.read_file(file_path)
    df = pd.DataFrame(read_fp)
    df = df.drop(['geometry','LC_PLY_PID'], axis =1)
    df.insert(2,'minx',0)
    df.insert(3,'miny',0)
    df.insert(4,'maxx',0)
    df.insert(5,'maxy',0)

    for idx, row in enumerate(read_fp.geometry.bounds.iterrows()):
        df.iat[idx,2] = row[1][0]
        df.iat[idx,3] = row[1][1]
        df.iat[idx,4] = row[1][2]
        df.iat[idx,5] = row[1][3]
    return df
suburbs = get_region(fp)

# print(float(suburbs.loc[suburbs['NAME'] == 'BUNDOORA']['minx']))

def auth_twitter():
    # authorize the API Key
    auth = tweepy.OAuthHandler(api_key, api_secret_key)

    # authorization to user's access token and access token secret
    auth.set_access_token(access_token, access_token_secret)

    # call the api
    api = tweepy.API(auth, wait_on_rate_limit=True)

keywords = ['house price','housing price']


class MyStreamListener(tweepy.Stream):
    
    def on_data(self, data):
        
        try: 
            tweet = json.loads(data)

        except Exception:
            print("Failed to parse tweet")
            tweet = None

        print(tweet['text'])


def streamtweets():
    minx = float(suburbs.loc[suburbs['NAME'] == 'BUNDOORA']['minx'])
    miny = float(suburbs.loc[suburbs['NAME'] == 'BUNDOORA']['miny'])
    maxx = float(suburbs.loc[suburbs['NAME'] == 'BUNDOORA']['maxx'])
    maxy = float(suburbs.loc[suburbs['NAME'] == 'BUNDOORA']['maxy'])

    auth_twitter()
    myStreamListener = MyStreamListener(api_key,api_secret_key,access_token,access_token_secret)
    myStreamListener.filter(track=keywords, languages =['en'], locations=[minx,miny,maxx,maxy])

streamtweets()

