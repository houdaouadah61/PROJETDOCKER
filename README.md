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
## Step 2.3.2 - Weather producer (Open-Meteo -> Kafka)
Kafka topic: `weather_transformed`

Kafka listeners:
- From containers (Jupyter, etc.): `kafka:29092`
- From host (Windows): `localhost:9092`

Install Python deps in the Jupyter container:
```bash
docker exec -it jupyter pip install --no-cache-dir kafka-python requests

