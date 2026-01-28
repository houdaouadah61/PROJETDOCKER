## Pipeline Big Data — Résumé des étapes

### Étape 1 — Infrastructure Docker
Mise en place d’une architecture Big Data avec Docker Compose incluant Hadoop (NameNode/DataNode), Spark (master/worker), Kafka et un environnement Jupyter.

### Étape 2 — Streaming météo vers Kafka
Implémentation d’un producteur qui récupère des données météo via l’API Open-Meteo, applique une transformation (température en Fahrenheit, alerte vent fort) puis publie les messages dans un topic Kafka.

### Étape 3 — Agrégation Spark
Création d’un job Spark Structured Streaming qui lit le topic Kafka, reconstruit le schéma JSON, et calcule sur une fenêtre d’1 minute :
- la température moyenne
- le nombre d’alertes “vent fort”

### Étape 4 — Export HDFS
Extension du job Spark pour sauvegarder les résultats dans HDFS au format CSV (création automatique du dossier cible si nécessaire).

### Étape finale — Orchestration Airflow
Ajout d’Airflow et création d’un DAG permettant d’orchestrer l’exécution du traitement (soumission du job Spark) et de vérifier l’écriture des résultats dans HDFS.
Les détails de cette partie sont décrits dans `docs/final_steps.md`.
