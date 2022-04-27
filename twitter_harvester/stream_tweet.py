import json
import tweepy
import database
from shapely.geometry import Polygon
from shapely.geometry import Point



api_key = 'RF78G9kS9YenS6eB6GEwcXg4o'
api_secret_key = '7yl0aW8s4Mg5dZgCMMamlTQ1SIN40frPlpin6Vnwb0TZGvRRnp'
access_token = '1343516103222251522-ITVMH6zGvtjmfSOGlGeN7j7JY9wATM'
access_token_secret = 'whImRAgACzng0PT4OyU6lb90KIxbU4V0YxxxGUpcGko5s'

suburbs_poly = '/Users/belkok/Documents/GitHub/COMP90024/COMP90024_A2/data/housing_type.json'

couch_database = database.create_database('harvest')

# authentication
def auth_twitter():
    # authorize the API Key
    auth = tweepy.OAuthHandler(api_key, api_secret_key)

    # authorization to user's access token and access token secret
    auth.set_access_token(access_token, access_token_secret)

    # call the api
    api = tweepy.API(auth, wait_on_rate_limit=True)

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
    
    if tweet['coordinates'] != None:
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
        couch_database.save({'id': tweet['id'], 'suburb': suburb, 'text': tweet.text})
        # print(suburb,tweet['text'],tweet['id'])
  
# class for twitter stream
class MyStreamListener(tweepy.Stream):
    
    def on_data(self, data):
        
        try: 
            tweet = json.loads(data)

        except Exception:
            print("Failed to parse tweet")
            tweet = None

        if 'RT @' not in tweet['text']:
            parse_tweet(tweet)

    def on_error(sefl, status_code):
        if status_code ==420:
            return False
        else:
            return True

MELBOURNE_BOUNDARY = [144.3336,-38.5030,145.8784,-37.1751]

def streamtweets():
    auth_twitter()
    myStreamListener = MyStreamListener(api_key,api_secret_key,access_token,access_token_secret)
    myStreamListener.filter(languages =['en'], locations=MELBOURNE_BOUNDARY)

streamtweets()


