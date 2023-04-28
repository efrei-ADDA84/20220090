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