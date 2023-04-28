# TP1 20220090 Mathis Da Cruz 

## Questions

* Créer un repository Github avec pour nom votre identifiant EFREI
* Créer un wrapper qui retourne la météo d'un lieu donné avec sa latitude et sa longitude
(passées en variable d'environnement) en utilisant openweather API dans le langage de
programmation de votre choix (bash, python, go, nodejs, etc)
* Packager son code dans une image Docker
* Mettre à disposition son image sur DockerHub
* Mettre à disposition son code dans un repository Github

Tester l'API openweather [ici](https://api.openweathermap.org/data/2.5/weather?lat=-31.2504&lon=-99.2506&appid=2161992f8e11948a5c0804c922c44d1b&units=metric)

## 1. Script Python

Libraries utilisées :

```
import os
import requests
```

Récupérer les variables d'environnement saisies avec la librairie os

```
lat = os.environ.get('LAT')
lon = os.environ.get('LONG')
api_key = os.environ.get('API_KEY')
```

Fonction permettant de construire une URL qui sera utilisée pour interroger l'API OpenWeatherMap et récupérer la météo pour un lieu donné. 
Metrique permet d'utiliser le Celcius pour exprimer les températures.

```
def get_url(lat, lon, api_key):
    return f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric'   
```

Fonction pour envoyer une requête HTTP GET à l'API et récupérer les données de la réponse.
Une fois que la réponse est récupérée, elle est convertie en format JSON.

```
def get_weather(url):
    response = requests.get(url)
    return response.json()  
```

Affichage du résultat :

```
print(get_weather(get_url(lat, lon, api_key)))
```

---

## 2. Dockerfile

```
FROM python:3.9.7
WORKDIR /app
COPY tp1.py /app
COPY requirement.txt /app
RUN python -m pip install -r requirement.txt
CMD python tp1.py
```

* On définit notre version de python
* On définit un espace de travail app
* On copie les fichiers créés précédemments et on les colle dans app
* On installe les pip requis pour l'exécution de notre script
* On excécute notre script

---

## 3. Dockerhub

On construit une nouvelle image Docker en se basant sur le contenu du Dockerfile présent dans le répertoire courant

```
docker build -t tp1_image:0.1 .
```

On renomme l'image afin de préparer l'image à être téléchargée sur DockerHub

```
docker tag tp1_image:0.1  mathisdacruz/tp1:0.1
```

On publie l'image sur DockerHub

```
docker push mathisdacruz/tp1:0.1
```

On lance un conteneur à partir de l'image Docker en definissant les variables d'environnement

```
docker run --env LAT="31.2504" --env LONG="-99.2506" --env API_KEY="2161992f8e11948a5c0804c922c44d1b" mathisdacruz/tp1:0.1
```