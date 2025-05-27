from flask import Flask, request, jsonify
from datetime import datetime,timezone
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb+srv://ffjokerking580:<db_password>@cluster0.jdngqvd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # Replace with your MongoDB URI if remote
db = client["my_database"]
collection = db["EM"]

@app.route('/', methods=['GET'])
def main():
    return jsonify({'msg': 'API Working'})

@app.route('/receive-location', methods=['POST'])
def receive_location():
    data = request.json

    # Create a document to insert
    document = {
        "device_name": data.get('device_name', 'unknown'),
        "timestamp": data.get('timestamp', str(datetime.utcnow())),
        "location": data.get('location', {}),
        "extra_info": data.get('extra_info', {}),
        "received_at": datetime.now(timezone.utc)  # server-side timestamp
    }

    # Insert into MongoDB
    collection.insert_one(document)

    return {"status": "received"}, 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
