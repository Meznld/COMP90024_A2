
import json
import database
from shapely.geometry import Polygon
from shapely.geometry import Point

# put huge data on the server and change the filepath
huge_data = '/Users/belkok/OneDrive/Uni Melb/2022 semester 1/COMP90024/Assignment/twitter-melb.json'
suburbs_poly = 'data/housing_type.json'

# get suburbs from json housing file
def get_suburbs(json_file):
    # open json file
    read_json = json.load(open(json_file))

    # list comprehension to get suburbs 
    suburb_list = [x['properties']['sa2_name16'] for x in read_json['features']]

    return suburb_list, read_json

couch_database = database.create_database('augment')
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

with open(huge_data) as f:
    for val in f:
        try:
            tweet = json.loads(val[0:-2])
            suburb = find_suburb(tweet['doc']['geo']['coordinates'][1],tweet['doc']['geo']['coordinates'][0])
            couch_database.save({'id': tweet['doc']['id'], 'suburb': suburb, 'text': tweet['doc']['text']})
            # print(find_suburb(tweet['doc']['geo']['coordinates'][1],tweet['doc']['geo']['coordinates'][0]),tweet['doc']['text'],tweet['doc']['id'])
            
        except:
            continue    
