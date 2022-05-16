import json
import os

def process():
    '''
    Class : Suburb name, Pos, Neg, Neutral
    HashSet to store Class
    Sort HashSet by % of positive
    Return list of top 10 : {suburbnam : % of positive}
    '''
    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    set = {}
    with open(os.path.join(__location__, 'test.json')) as json_file:
        data = json.load(json_file)
    
        for i in data['rows']:
            suburb = i['key'][0]
            sentiment = i['key'][1]
            value = i['value']
            print (suburb + " " + sentiment +  " ")
            print (value)
            


    #return data

class Suburb:
    def __init__(self, name):
        self.suburb = name
        self.negative = 0
        self.neutral = 0
        self.positive = 0

process()