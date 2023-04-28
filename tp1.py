import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

api_key = os.environ.get('API_KEY')

def get_url(lat, lon, api_key):
    return f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric'   

def get_weather(url):
    response = requests.get(url)
    return response.json()  

@app.route('/weather')
def weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    url = get_url(lat, lon, api_key)
    weather_data = get_weather(url)
    return jsonify(weather_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port= 8081)