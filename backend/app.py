from flask import Flask, render_template, jsonify
from flask_cors import CORS
import geopandas as gpd
import pandas as pd
import requests
import json

app = Flask(__name__)
CORS(app)

# load aurin data in the json file as a dataframe of properties, so that it can be merged to the shapefile properties
with open(".\static\SA2-G02_Selected_Medians_and_Averages-Census_2016.json\sa2_g02_selected_medians_and_averages_census_2016-7286388448228732680.json") as f:
    data = json.load(f)
ldf = list()
for item in data["features"]:
    ldf.append(item["properties"])
df = pd.DataFrame(ldf)

@app.route("/")
def hello_world():
    return ("Hello!")

# shapefile data
@app.route("/geopandas")
def geopandas():
    house_type = gpd.read_file(r"static\spatialise-rent\shp\sa2_p02_selected_medians_and_averages_census_2016-.shp")
    output = house_type.to_json()
    return output

# data with merged properties of aurin and shapefile
@app.route("/aurin")
def aurin():
    house_type = gpd.read_file(r"static\spatialise-rent\shp\sa2_p02_selected_medians_and_averages_census_2016-.shp")
    result = house_type.merge(df, on="sa2_main16")
    output = result.to_json()
    return output

@app.route("/testGet2")
def testGet2():
    uri = "http://user:pass@172.26.132.238:5984/data/_design/data/_view/test?group=true"
    try:
        uResponse = requests.get(uri)
        Jresponse = uResponse.text
        data = json.loads(Jresponse)
        output = data
        print(type(output))
    except requests.ConnectionError:
       return "Connection Error"

    return output

# data sorted according to value, it takes a bit long to sort (about 30s on my computer)
@app.route("/testGet2/sorted")
def testGet2_top10positive():
    uri = "http://user:pass@172.26.132.238:5984/data/_design/data/_view/test?group=true"
    try:
        uResponse = requests.get(uri)
        Jresponse = uResponse.text
        data = json.loads(Jresponse)
        #output = data
        output = data
        output["rows"] = sorted(data["rows"], key = lambda item: item['value'], reverse = True)
    except requests.ConnectionError:
       return "Connection Error"
    
    return output

@app.route("/testGetTopic/<str>")
def testGetTopic(str):
    uri = ""
    if (str == "crypto"):
        uri = "http://admin:XlkLSNezrwOlQ0fIx5C@172.26.128.201:30396/crypto/_design/aggregate/_view/suburb?group=true"
    elif (str == "covid"):
        uri = "http://admin:XlkLSNezrwOlQ0fIx5C6@172.26.128.201:30396/covid/_design/aggregate/_view/suburb?group=true"
    elif (str == "housing"):
        uri = "http://admin:XlkLSNezrwOlQ0fIx5C6@172.26.128.201:30396/housing/_design/aggregate/_view/suburb?group=true"
    elif (str == "election"):
        uri = "http://admin:XlkLSNezrwOlQ0fIx5C6@172.26.128.201:30396/election/_design/aggregate/_view/suburb?group=true"
    elif (str == "harvest"):
        uri = "http://admin:XlkLSNezrwOlQ0fIx5C6@172.26.128.201:30396/harvest/_design/aggregate/_view/suburb?group=true"

    try:
        uResponse = requests.get(uri)
        Jresponse = uResponse.text
        data = json.loads(Jresponse)
        output = data
    except requests.ConnectionError:
       return "Connection Error"

    return output

if __name__ == '__main__':
    app.debug=True
    app.run()

'''
login page: http://172.26.132.238:5984/_utils/index.html#login
'''