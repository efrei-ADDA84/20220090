import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

def get_url(lat, lon):
    return f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=2161992f8e11948a5c0804c922c44d1b&units=metric'   

def get_weather(url):
    response = requests.get(url)
    return response.json()  

@app.route('/')
def weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    url = get_url(lat, lon)
    weather_data = get_weather(url)
    return jsonify(weather_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port= 8081)