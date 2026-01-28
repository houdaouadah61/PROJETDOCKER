# Big Data Docker Compose — Étape 1

## Lancer Jupyter
```bash
docker compose up -d
## Step 2.2 - Kafka Producer/Consumer test
Topic: weather  
Messages received by consumer:
- {"city":"Paris","temp":12}
- {"city":"Rabat","temp":18}
## Step 2.3.1 - Jupyter dependencies (Kafka Producer)
Inside Jupyter, install Python dependencies:
```bash
pip install kafka-python requests

