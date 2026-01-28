# PROJETDOCKER — Pipeline de données météo avec Kafka, Spark, HDFS et Airflow

## Objectif du projet

L’objectif de ce projet est de mettre en place un pipeline de données complet, conteneurisé avec Docker, permettant :

- d’ingérer des données météo,
- de les traiter avec Apache Spark,
- de stocker les résultats dans HDFS,
- et d’orchestrer l’exécution avec Apache Airflow.

---

## Étape 1 — Mise en place de l’environnement Docker

Une architecture Docker Compose a été créée afin de déployer les services suivants :

- Apache Kafka pour l’ingestion des données,
- Apache Spark (mode standalone) pour le traitement distribué,
- Hadoop HDFS (NameNode et DataNode) pour le stockage,
- Apache Airflow avec PostgreSQL pour l’orchestration,
- Jupyter Notebook pour les tests et le développement.

Tous les services communiquent via un réseau Docker commun.

---

## Étape 2 — Ingestion des données météo

Un producteur Kafka a été développé afin d’envoyer des données météo simulées au format JSON dans un topic Kafka dédié.

Chaque message contient notamment :
- un timestamp,
- une température,
- un indicateur d’alerte éventuel.

---

## Étape 3 — Traitement des données avec Spark

Un script Spark a été implémenté pour :

- lire les messages depuis le topic Kafka,
- parser les données JSON,
- appliquer une agrégation par fenêtres temporelles (window),
- calculer :
  - la température moyenne,
  - le nombre d’alertes par fenêtre.



---

## Étape 4 — Stockage des résultats dans HDFS

Les résultats agrégés par Spark sont écrits dans HDFS :

- au format CSV,
- dans un répertoire dédié,
- avec génération automatique des fichiers `part-*.csv`.

## Étape 5 — Orchestration avec Apache Airflow

Un DAG Airflow nommé `weather_pipeline` a été créé afin de :

- déclencher automatiquement le job Spark,
- superviser son exécution,
- gérer les erreurs et les états des tâches.


