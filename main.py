import requests
from datetime import datetime
import socket

API_URL = "http://192.168.192.201:5000/receive-location"  # Replace with your actual server IP and port

def get_ip_location():
    try:
        response = requests.get("http://ip-api.com/json/")
        data = response.json()
        if data["status"] == "success":
            return {
                "lat": data["lat"],
                "lon": data["lon"],
                "city": data.get("city", ""),
                "region": data.get("regionName", ""),
                "country": data.get("country", "")
            }
        else:
            print("Failed to get location:", data.get("message"))
            return None
    except Exception as e:
        print("Error fetching IP location:", e)
        return None

def send_location_to_api(location):
    payload = {
        "device_name": socket.gethostname(),
        "timestamp": datetime.utcnow().isoformat(),
        "location": {
            "lat": location["lat"],
            "lon": location["lon"]
        },
        "extra_info": {
            "city": location.get("city"),
            "region": location.get("region"),
            "country": location.get("country")
        }
    }
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            print("Location sent successfully.")
        else:
            print("Failed to send location, status code:", response.status_code)
    except Exception as e:
        print("Error sending location:", e)

def main():
    location = get_ip_location()
    if location:
        print(f"Got location: {location}")
        send_location_to_api(location)
    else:
        print("Could not get location.")

if __name__ == "__main__":
    main()
