\## Étape 5 — Orchestration avec Apache Airflow (Étape finale)



Cette dernière étape consiste à orchestrer l’ensemble du pipeline Big Data à l’aide d’Apache Airflow.



Airflow a été ajouté à l’architecture Docker afin de piloter automatiquement l’exécution du traitement Spark.



Un DAG nommé `weather\_pipeline` a été créé. Il permet de :

\- déclencher l’exécution du job Spark,

\- surveiller son état (succès ou échec),

\- garantir l’exécution complète du pipeline.



Le job Spark est soumis au cluster Spark (mode standalone) depuis Airflow et traite les données météo provenant de Kafka.



Les résultats agrégés sont ensuite sauvegardés dans HDFS au format CSV dans le répertoire :

`/user/jovyan/weather\_csv`.



L’exécution du DAG a été validée via l’interface web d’Airflow, avec un statut \*\*SUCCESS\*\*, confirmant le bon fonctionnement du pipeline de bout en bout.



