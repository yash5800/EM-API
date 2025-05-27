# send_location.py
import subprocess, requests, socket, json
from datetime import datetime

ip = '192.168.207.201'

API_URL = f"http://{ip}:5000/receive-location"

def get_location():
    try:
        loc = subprocess.check_output(["termux-location", "--provider", "network", "--request", "once"])
        return json.loads(loc.decode())
    except:
        return None

def send_location():
    data = get_location()
    if data:
        payload = {
            "device_name": socket.gethostname(),
            "timestamp": datetime.utcnow().isoformat(),
            "location": {
                "lat": data["latitude"],
                "lon": data["longitude"]
            }
        }
        print("Sending:", payload)
        try:
            r = requests.post(API_URL, json=payload)
            print("Status:", r.status_code)
        except Exception as e:
            print("Error:", e)
    else:
        print("Location unavailable")


send_location()