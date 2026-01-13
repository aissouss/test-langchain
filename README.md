
# 📦 Weather Agent – LangChain (Option B)

## 📌 Description du projet

Ce projet consiste à développer un **agent météo intelligent** en Python à l’aide de **LangChain**.
L’agent est capable de répondre aux questions météo de l’utilisateur en **temps réel**, en utilisant de **vraies données météorologiques** issues d’une API publique.

Le projet s’appuie sur le **quickstart officiel de LangChain**, puis l’enrichit conformément à **l’Option B : Enrichir les outils existants**.

---

## 🛠️ Prérequis

* Python **3.10 ou supérieur**
* Un compte **Anthropic (Claude)**
* Une clé API Anthropic valide

---

## 📚 Ressources

Documentation Open-Meteo (API météo) :
https://open-meteo.com/en/docs

Documentation Open-Meteo – API de géocodage :
https://open-meteo.com/en/docs/geocoding-api

Bibliothèque Python open-meteo (PyPI) :
https://pypi.org/project/open-meteo/

Bibliothèque Python openmeteo-requests (client officiel Open-Meteo) :
https://pypi.org/project/openmeteo-requests/

Tutoriel externe pour exploiter des données météo en Python :
https://www.geodose.com/2023/08/get-plot-weather-data-python.html

Documentation LangChain – Quickstart Python :
https://docs.langchain.com/oss/python/langchain/quickstart

---

## ⚙️ Installation et configuration

### 1️⃣ Installation des dépendances

```bash
pip install -U langchain
pip install -U langchain-anthropic
pip install requests requests-cache retry-requests openmeteo-requests
```

> ⚠️ Python était déjà installé sur la machine avant le projet.

---

### 2️⃣ Configuration de la clé API

La clé API Anthropic doit être définie dans les **variables d’environnement utilisateur** :

* **Nom de la variable :**

```text
ANTHROPIC_API_KEY
```

* **Valeur :**

```text
votre_cle_api_claude
```

Cette configuration permet à LangChain d’accéder au modèle Claude sans inclure la clé directement dans le code (bonne pratique de sécurité).

---

## 🚀 Lancement du projet

```bash
python agentmeteo.py
```

Une interface en ligne de commande s’ouvre.
L’utilisateur peut poser des questions météo sur différentes villes jusqu’à taper `exit` pour quitter.

---

## 🧠 Fonctionnement de l’agent

### 🔹 Prompt système

Le prompt a été adapté afin que l’agent :

* comprenne les demandes météo,
* détecte la ville mentionnée,
* utilise des outils pour récupérer des données **réelles**,
* réponde avec une touche humoristique tout en restant informative.

---

### 🔹 Structures de données

Deux **dataclasses** ont été introduites pour structurer proprement les données :

#### `LocationData`

* nom de la ville
* latitude
* longitude

#### `WeatherData`

* température
* humidité
* vitesse du vent
* conditions météo

Le choix des dataclasses améliore la lisibilité, la structure et la maintenabilité du code par rapport à un simple dictionnaire.

---

### 🔹 Outil `get_user_location`

* Convertit le nom d’une ville en coordonnées géographiques
* Utilise l’API de **géocodage Open-Meteo**
* Vérifie si la ville existe
* Extrait le **premier résultat** retourné
* Retourne un objet `LocationData`

---

### 🔹 Outil `get_weather_for_location`

* Récupère la météo actuelle à partir des coordonnées
* Utilise l’API **Open-Meteo** avec :

  * cache des requêtes
  * mécanisme de retry
* Retourne :

  * température
  * humidité
  * vitesse du vent
  * état du ciel

Les données sont encapsulées dans un objet `WeatherData`.

---

### 🔹 Agent LangChain et mémoire

* Le modèle Claude est conservé tel que dans le quickstart
* Une mémoire conversationnelle en RAM (`InMemorySaver`) est utilisée
* L’agent peut répondre à plusieurs questions successives dans une même session

---

## 🧪 Exemple d’utilisation

**Entrée utilisateur :**

```
What is the weather in Paris?
```

**Sortie possible :**

```
Agent: Looks like Paris is having a sun-sational day!
Données: Temperature: 22°C | Sunny | Humidity: 65% | Wind: 12 km/h
```

📸 Des captures d'écran sont disponibles dans le dépôt GitHub.

---

## ⚠️ Difficultés rencontrées et solutions

### 🔸 Utilisation de l’API météo

* La documentation fournissait des exemples partiels
* Il a fallu comprendre la structure des réponses API et adapter les appels REST

### 🔸 **Optimisation de la récupération des données météo (amélioration apportée)**

**Problème principal identifié :**
Le code initial utilisait `current_weather=True` combiné avec
`hourly="relative_humidity_2m"`.
Cette approche téléchargeait **168 heures de données (7 jours)** uniquement pour récupérer l’humidité actuelle, tout en mélangeant deux sources de données (`current` et `hourly`).

**Solution implémentée :**
Migration vers le format moderne de l’API Open-Meteo :

```json
"current": [
  "temperature_2m",
  "wind_speed_10m",
  "relative_humidity_2m",
  "weather_code"
]
```

Cette approche permet d’obtenir toutes les données actuelles en **un seul appel cohérent**, avec un **ordre garanti** des variables.

**Autres améliorations :**

* Extension du mapping des codes météo (10 → 27 codes WMO)
* Correction d’un bug d’affichage lors des comparaisons multi-villes
* Amélioration du system prompt

### 🔸 Géolocalisation

* La météo nécessite des coordonnées GPS
* Une API de géocodage a été intégrée pour convertir les villes en latitude/longitude

### 🔸 Structuration des données

* Passage de chaînes simples à des données structurées
* Les `dataclasses` ont permis une solution propre et maintenable

L’utilisation de la documentation officielle et d’assistants IA (ChatGPT, Claude) a permis de lever certaines incompréhensions et d’approfondir la compréhension des APIs.

---

## ✅ Option choisie : **Option B – Enrichir les outils existants**

### 🎯 Justification

L’Option B permet de donner une **véritable utilité** à l’agent météo.
L’utilisation de données réelles rend l’agent plus pertinent qu’une simple simulation.

* Réponses possibles pour n’importe quelle ville
* Données structurées
* Interaction naturelle en ligne de commande

---

## 🏁 Conclusion

Ce projet m’a permis :

* de suivre et comprendre un tutoriel LangChain,
* d’adapter un code existant,
* d’intégrer des APIs externes,
* et de concevoir un agent IA plus réaliste.

---

**Note :** le contenu de ce README est basé sur mon travail personnel ; ChatGPT a uniquement servi à reformuler et améliorer la qualité rédactionnelle.

---


