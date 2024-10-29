from flask import Flask, jsonify, render_template
import requests
import os
from dotenv import load_dotenv
import json

app = Flask(__name__)

load_dotenv()
API_URL = os.getenv('API_URL')
GEO_API_URL = os.getenv('GEO_API_URL')
API_KEY = os.getenv('API_KEY')
CITY = os.getenv('CITY')
COUNTRY = os.getenv('COUNTRY')

def get_coordinates_for_city():
    res = requests.get(GEO_API_URL, params={
        "q": f"{CITY},{COUNTRY}",
        "appid": API_KEY
    }).json()

    print(res)

    if res and isinstance(res, list) and len(res) > 0:
        lat = res[0]["lat"]
        lon = res[0]["lon"]

        return lat, lon
    else:
        raise ValueError("No coordinates found.")

coordinates = get_coordinates_for_city()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/weather/current')
def get_weather():
    lat, lon = coordinates

    res = requests.get(API_URL, params={
        "lat": lat,
        "lon": lon,
        "units": "metric",
        "appid": API_KEY
    }).json()

    weather_data = {
        "temp": res["main"]["temp"],
        "feels_like": res["main"]["feels_like"],
        "description": res["weather"][0]["description"],
        "wind_speed": res["wind"]["speed"]
    }
    print(weather_data)

    return jsonify(weather_data)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)