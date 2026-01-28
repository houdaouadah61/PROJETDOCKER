import json
import time
import requests
from kafka import KafkaProducer

API_URL = "https://api.open-meteo.com/v1/forecast"
LAT, LON = 52.52, 13.41  # Berlin (exemple)
TOPIC = "weather_transformed"

# Depuis le conteneur Jupyter, Kafka est accessible via le nom de service docker-compose
BROKER = "kafka:9092"

def fetch_weather():
    params = {"latitude": LAT, "longitude": LON, "current_weather": "true"}
    r = requests.get(API_URL, params=params, timeout=10)
    r.raise_for_status()
    return r.json().get("current_weather", {})

def transform(record: dict) -> dict:
    out = dict(record)
    if "temperature" in out:
        out["temp_f"] = out["temperature"] * 9 / 5 + 32
    out["high_wind_alert"] = out.get("windspeed", 0) > 10
    return out

def main():
    producer = KafkaProducer(
        bootstrap_servers=BROKER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    print(f"Producer started. Broker={BROKER} Topic={TOPIC}")

    while True:
        try:
            w = fetch_weather()
            if w:
                msg = transform(w)
                producer.send(TOPIC, msg)
                producer.flush()
                print("Sent:", msg)
        except Exception as e:
            print("Error:", e)

        time.sleep(30)

if __name__ == "__main__":
    main()
