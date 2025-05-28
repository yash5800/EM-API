from flask import Flask, request, jsonify
from datetime import datetime,timezone
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB connection
client = MongoClient(os.getenv('mongodb'))  # Replace with your MongoDB URI if remote
db = client["my_database"]
collection = db["EM"]


@app.route('/', methods=['GET'])
def main():
    return jsonify({'msg': 'API Working'})
  
  
@app.route('/receive-location', methods=['POST'])
def receive_location():
    data = request.json
    
    doc = {
        "device_name": data['device_name'],
        "timestamp": data['timestamp'],
        "location": data['location'],
        "extra_info": data['extra_info'],
    }
    
    collection.insert_one(doc)

    return {"status": "received"}, 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
