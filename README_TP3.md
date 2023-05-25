# TP2 20220090 Mathis Da Cruz 

## Questions

* Configurer un workflow Github Action
* Transformer un wrapper en API
* Publier automatiquement a chaque push sur Docker Hub
* Mettre à disposition son image (format API) sur DockerHub
* Mettre à disposition son code dans un repository Github

---

## 1. Workflow

Nom de l'action et son périmètre, ici branche main

```
name: Build and Push

on:
  push:
    branches: [main]
```
Nature de la tache (build and publish) et a executer sur ubuntu

```
jobs:
  build-and-publish:
    runs-on: ubuntu-latest
```

Etapes:
1. On recupere le code source

```
    steps:
      - name: Checkout
        uses: actions/checkout@v2
```

2. On build l'image 

```
      - name: Build
        run: docker build -t tp2_image:0.2.2 .
```

3. Connexion a docker a l'aide des infos d'identification stockées dans les secrets GitHub.

```
      - name: Login
        uses: docker/login-action@v1
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
```

4. On push l'image sur Docker

```
      - name: Push
        uses: docker/build-push-action@v2
        with:
          context: .
          push: true
          tags: mathisdacruz/tp1:0.2.2
```

Apres verification sur github action, la tache a bien ete effectue suite au commit !

---

## 2. API

On repart du script python du tp1 en ajoutant quelques modifications
Avec la librairies Flask on crée une application web

```
from flask import Flask, jsonify, request
app = Flask(__name__)
```

* @app.route('/weather') : Décorateur de fonction Flask qui définit une route pour l'API (url/weather)
* lat = request.args.get('lat') : On recupere l'argument de lat dans l'url afin d'appeler l'API avec

```
@app.route('/weather')
def weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    url = get_url(lat, lon, api_key)
    weather_data = get_weather(url)
    return jsonify(weather_data)
```

* debug=True : mode de débogage de Flask
* host='0.0.0.0' : l'adresse IP est définie sur "0.0.0.0", donc depuis le localhost
* port=8081 : définit le port sur lequel Flask doit écouter les requêtes entrantes

```
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port= 8081)
```
---

## 3. Commandes Docker

On specifie le port 8081 defini precedemment

```
docker build -t tp2_image:0.2.2 .
docker tag tp2_image:0.2.2 mathisdacruz/tp1:0.2.2
docker push mathisdacruz/tp1:0.2.2
docker run -p 8081:8081 --env API_KEY="2161992f8e11948a5c0804c922c44d1b" mathisdacruz/tp1:0.2.2
```

La commande suivante fonctionne bien

```
curl "http://localhost:8081/weather?lat=5.902785&lon=102.754175"
```

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
  "dt": 1682688551,
  "id": 1736405,
  "main": {
    "feels_like": 30.3,
    "grnd_level": 981,
    "humidity": 76,
    "pressure": 1008,
    "sea_level": 1008,
    "temp": 27.45,
    "temp_max": 27.45,
    "temp_min": 27.45
  },
  "name": "Jertih",
  "sys": {
    "country": "MY",
    "sunrise": 1682636226,
    "sunset": 1682680546
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
    "deg": 78,
    "gust": 4.07,
    "speed": 3.78
  }
}
```