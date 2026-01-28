# Résumé des étapes réalisées (Kafka + météo)

## Step 2.1 — Mise en place de Kafka (mode KRaft) + création d’un topic
- Ajout de Kafka dans `docker-compose.yml` (mode **KRaft**, donc sans ZooKeeper).
- Démarrage de la stack avec Docker Compose.
- Création et vérification d’un premier topic Kafka nommé `weather`.

---

## Step 2.2 — Vérification du fonctionnement Kafka (Producer / Consumer)
- Test du pipeline Kafka avec les outils en ligne de commande :
  - lancement d’un **consumer** sur le topic `weather`,
  - lancement d’un **producer** et envoi de messages,
  - vérification que les messages sont bien consommés.
- Objectif : valider que Kafka fonctionne correctement avant d’ajouter du code Python.

---

## Step 2.3.1 — Préparation de l’environnement Python (dans Jupyter)
- Installation des dépendances nécessaires dans le conteneur Jupyter :
  - `kafka-python` pour produire dans Kafka,
  - `requests` pour appeler une API HTTP.
- Objectif : permettre l’exécution d’un producer Python dans l’environnement Jupyter.

---

## Step 2.3.2 — Producer météo (Open-Meteo → Kafka) + transformation des données
- Création d’un second topic Kafka : `weather_transformed`.
- Écriture d’un script Python (`weather_producer.py`) qui :
  - récupère des données météo via l’API **Open-Meteo**,
  - transforme les données (ex. conversion température + ajout d’un indicateur d’alerte vent),
  - envoie les messages transformés dans Kafka (`weather_transformed`).
- Ajustement de la configuration Kafka avec **deux listeners** :
  - un pour la machine hôte (Windows),
  - un pour les conteneurs Docker (communication interne entre services).
- Vérification avec un consumer Kafka que les messages arrivent bien sur `weather_transformed`.
## Step 3 - Spark : agrégation sur fenêtre 1 minute
Objectif : calculer la température moyenne et le nombre d’alertes de vent fort sur une fenêtre temporelle d’1 minute à partir du topic Kafka `weather_transformed`.

- Script : `src/weather_spark.py`
- Spark master : `spark://spark-master:7077` (pas de `local[*]`)
- Kafka (depuis conteneurs) : `kafka:29092`
- Sortie : affichage console via `show()` (exemple du PDF)
## Step 3 — Traitement Spark (agrégation)

Objectif : lancer un job Spark qui lit les messages du topic Kafka `weather_transformed` et calcule une agrégation par fenêtre de 1 minute.

### Démarrage du cluster Spark
- Ajout de `spark-master` et `spark-worker` dans `docker-compose.yml`
- Spark UI :
  - Master : http://localhost:8080
  - Worker : http://localhost:8081

### Exécution du job Spark
Le script Spark est placé dans `notebooks/weather_spark.py` (monté dans le conteneur Spark via un volume).

Commande utilisée (avec le connecteur Kafka) :

```bash
docker exec -it spark-master /spark/bin/spark-submit --master spark://spark-master:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1 /workspace/weather_spark.py
