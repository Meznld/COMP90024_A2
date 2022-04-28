import json
import tweepy
import couchdb
import os
from shapely.geometry import Polygon
from shapely.geometry import Point


credentials = os.path.join(os.path.dirname(os.path.abspath(__file__)), "credentials.json")
suburbs_poly = os.path.join(os.path.dirname(os.path.abspath(__file__)), "housing_type.json")

# initialize coucbdb
couch = couchdb.Server('http://admin:XlkLSNezrwOlQ0fIx5C6@172.26.128.201:30396/')
try:
    couch_database = couch.create('harvest')
except:
    couch_database = couch['harvest']


def get_credentials(credentials_file):
    read_json = json.load(open(credentials))
    stream = {}
    for cred in read_json['stream']:
        stream.update({cred: read_json['stream'][cred]})
    search = []
    for cred in read_json['search']:
        search.append(cred) 
    return stream, search
    
stream, search = get_credentials(credentials)

# authentication

api_list=[]

def authentications():
    # authenticate stream
    auth = tweepy.OAuthHandler(stream['api_key'], stream['api_secret'])
    auth.set_access_token(stream['access_token'], stream['access_secret'])

    # authenticate search
    for each in search:
        auth = tweepy.OAuthHandler(each['api_key'],each['api_secret'])
        api = tweepy.API(auth, wait_on_rate_limit=True)
        api_list.append(api)

# get suburbs from json housing file
def get_suburbs(json_file):
    # open json file
    read_json = json.load(open(json_file))

    # list comprehension to get suburbs 
    suburb_list = [x['properties']['sa2_name16'] for x in read_json['features']]

    return suburb_list, read_json

suburbs, boundary_file = get_suburbs(suburbs_poly)

SINGLE = 'Polygon'
MULTI = 'MultiPolygon'
# get suburb of tweet
def find_suburb(long, lat):
    # look through each suburb block
    for sub in boundary_file['features']:

        # if shape is a multipolygon go through each polygon
        if sub['geometry']['type'] == MULTI:
            for each in sub['geometry']['coordinates']:

                # if point is in polygon return suburb
                if Polygon(each[0]).contains(Point([long,lat])):
                    return sub['properties']['sa2_name16']

        # if shape is a single polygon
        elif sub['geometry']['type'] == SINGLE:

            # if point is in polygon return suburb
            if Polygon(sub['geometry']['coordinates'][0]).contains(Point([long,lat])):
                return sub['properties']['sa2_name16']
    return None

# parse json tweet from stream and store in couchdb
def parse_tweet(tweet):
    suburb = None
    if tweet['coordinates'] != None:

        if type(tweet['coordinates']) is dict:

            suburb = find_suburb(tweet['coordinates']['coordinates'][0],tweet['coordinates']['coordinates'][1])

        else:

            suburb = find_suburb(tweet['coordinates'][0],tweet['coordinates'][1])

    else:
        try:
            if tweet['place']['place_type'] == 'city':
                suburb = tweet['place']['name']
        except:
            suburb = None
            pass
    # store in couchdb
    if suburb != None:
        
        couch_database.save({'id': tweet['id'], 'suburb': suburb, 'text': tweet['text']})
        print("Tweet stored in CouchDB")
        # print(suburb,tweet['text'],tweet['id'])
        pass
  
# class for twitter stream
class MyStreamListener(tweepy.Stream):
    
    def on_data(self, data):
        
        try: 
            tweet = json.loads(data)
            print(tweet)
            if 'RT @' not in tweet['text']:
            	parse_tweet(tweet)
        except Exception:
            print("Failed to parse tweet")
            tweet = None

        

    def on_error(self, status_code):
        if status_code ==420:
            return False
        else:
            return True

MELBOURNE_BOUNDARY = [144.3336,-38.5030,145.8784,-37.1751]

def streamtweets():
    authentications()
    myStreamListener = MyStreamListener(stream['api_key'],stream['api_secret'],stream['access_token'],stream['access_secret'])
    myStreamListener.filter(languages =['en'], locations=MELBOURNE_BOUNDARY)

streamtweets()

# search historical tweets
maxId = None
while True:
    # use each credentials' api to search
    for api in api_list:
        tweets = tweepy.Cursor(api.search_tweets, q='-filter:retweets',lang='en', geocode='-37.840935,144.946457,60km', count=100, max_id=maxId)
        for each in tweets.items():
            tweet = each._json    
            maxId = tweet['id']-1
            parse_tweet(tweet)
     




