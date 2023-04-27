# 20220090
# TP1

# Script Python

# Libraries utilisées

import os
import requests

# Récupérer les variables d'environnement avec os

lat = os.environ.get('LAT')
lon = os.environ.get('LONG')
api_key = os.environ.get('API_KEY')

# Former l'url de notre API

def get_url(lat, lon, api_key):
    return f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric'   

# Requete sur l'API a partir de l'url, puis conversion du résultat en JSON

def get_weather(url):
    response = requests.get(url)
    return response.json()  

# Affichage du résultat

print(get_weather(get_url(lat, lon, api_key)))

# Valeur des paramètres

#lat = '31.2504'
#lon = '-99.2506'
#api_key = '2161992f8e11948a5c0804c922c44d1b'

#url = https://api.openweathermap.org/data/2.5/weather?lat=-31.2504&lon=-99.2506&appid=2161992f8e11948a5c0804c922c44d1b

# Dockerfile

FROM python:3.9.7
WORKDIR /app
COPY tp1.py /app
COPY requirement.txt /app
RUN python -m pip install -r requirement.txt
CMD python tp1.py

# Commande Dockerhub

docker build -t tp1_image .

docker tag tp1_image  mathisdacruz/tp1

docker push mathisdacruz/tp1

docker run --env LAT="31.2504" --env LONG="-99.2506" --env API_KEY="2161992f8e11948a5c0804c922c44d1b" mathisdacruz/tp1:latest