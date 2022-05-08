from flask import Flask, jsonify
import json
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


smallfilepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"static","smallfile.json")
with open(smallfilepath) as f:
    data = json.load(f)
#print(data)

@app.route('/file', methods=['GET'])
def get_filedata():
    #response = jsonify({'name': 'Hello'})
    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/")
def hello_world():
    return ("Hello!")

if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0')
