import os
import requests
from dotenv import load_dotenv

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def get_traffic_data(origin, destination, departure_time="now"):
    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": origin,
        "destinations": destination,
        "departure_time": departure_time,
        "traffic_model": "best_guess",
        "key": GOOGLE_MAPS_API_KEY,
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if data["status"] != "OK":
            raise ValueError(f"API Error: {data['status']}")

        element = data["rows"][0]["elements"][0]

        return {
            "origin": origin,
            "destination": destination,
            "duration": element["duration"]["text"],
            "duration_in_traffic": element["duration_in_traffic"]["text"],
            "distance": element["distance"]["text"],
        }

    except Exception as e:
        print(f"[ERROR] Failed to fetch traffic data: {e}")
        return None