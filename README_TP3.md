# TP3 20220090 Mathis Da Cruz 

## Objectifs

* Mettre à disposition son image (format API) sur Azure Container Registry (ACR) using
Github Actions
* Deployer sur Azure Container Instance (ACI) using Github Actions

---

## 1. Workflow

Le code suivant construit et déploie une image Docker sur une instance de conteneur Azure (ACI). 

Etapes:
* Il utilise l'action azure/login@v1 pour s'authentifier auprès d'Azure

```
name: Azure

on:
  push:
    branches:
      - main

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      - name: Login to Azure
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
```

* L'action azure/docker-login@v1 pour se connecter au registre de conteneurs
* Construit une image Docker et la pousse dans le registre de conteneurs. 

```
      - name: Build and push Docker image
        uses: azure/docker-login@v1
        with:
          login-server: ${{ secrets.REGISTRY_LOGIN_SERVER }}
          username: ${{ secrets.REGISTRY_USERNAME }}
          password: ${{ secrets.REGISTRY_PASSWORD }}
      - run: |
          docker build . -t ${{ secrets.REGISTRY_LOGIN_SERVER }}/20220090:v1
          docker push ${{ secrets.REGISTRY_LOGIN_SERVER }}/20220090:v1
```

* Déploie l'image sur une instance de conteneur Azure avec l'action azure/aci-deploy@v1.

```
      - name: Deploy to Azure Container Instance (ACI)
        uses: azure/aci-deploy@v1
        with:
          resource-group: ${{ secrets.RESOURCE_GROUP }}
          dns-name-label: devops-20220090
          image: ${{ secrets.REGISTRY_LOGIN_SERVER }}/20220090:v1
          registry-login-server: ${{ secrets.REGISTRY_LOGIN_SERVER }}
          registry-username: ${{ secrets.REGISTRY_USERNAME }}
          registry-password: ${{ secrets.REGISTRY_PASSWORD }}
          name: 20220090
          location: westeurope
          ports: 8081
```

---

## 2. Script Python

Modifications apportées au script python:
* Suppression de os.get_env pour récupérer l'api_key
* On code l'api_key en dure dans l'url et on l'enlève des paramètres des fonctions
* On enlève "weather" de @app.route

```
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

```

---

## 3. Résultat du curl

La commande suivante fonctionne bien

```
curl "http://devops-20220090.westeurope.azurecontainer.io:8081/?lat=5.902785&lon=102.754175"
```

On précise bien les paramètres propres a notre déploiement dans l'url:
* La localisation : west europe
* Le nom de domaine du DNS : devops-20220090
* Le numéro de port : 8081

Output

```
{
  "base": "stations",
  "clouds": {
    "all": 100
  },
  "cod": 200,
  "coord": {
    "lat": 5.9028,
    "lon": 102.7542
  },
  "dt": 1685032170,
  "id": 1736405,
  "main": {
    "feels_like": 30.66,
    "grnd_level": 985,
    "humidity": 71,
    "pressure": 1012,
    "sea_level": 1012,
    "temp": 27.93,
    "temp_max": 27.93,
    "temp_min": 27.93
  },
  "name": "Jertih",
  "sys": {
    "country": "MY",
    "sunrise": 1685055206,
    "sunset": 1685099928
  },
  "timezone": 28800,
  "visibility": 10000,
  "weather": [
    {
      "description": "overcast clouds",
      "icon": "04n",
      "id": 804,
      "main": "Clouds"
    }
  ],
  "wind": {
    "deg": 73,
    "gust": 2.06,
    "speed": 1.87
  }
}
```