import os
import requests

# Récupérer les variables d'environnement
lat = os.environ.get('LAT')
lon = os.environ.get('LONG')
api_key = os.environ.get('API_KEY')

#lat = '31.2504'
#lon = '-99.2506'
#api_key = '2161992f8e11948a5c0804c922c44d1b'

def get_url(lat, lon, api_key):
    return f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric'   

def get_weather(url):
    response = requests.get(url)
    return response.json()  

print(get_weather(get_url(lat, lon, api_key)))

#https://api.openweathermap.org/data/2.5/weather?lat=-31.2504&lon=-99.2506&appid=2161992f8e11948a5c0804c922c44d1b