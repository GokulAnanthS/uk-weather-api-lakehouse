import json
import uuid
import requests
from kafka import KafkaProducer
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

URL = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 51.5072,
    "longitude": -0.1276,
    "hourly": "temperature_2m,relative_humidity_2m"
}

response = requests.get(URL, params=params)

payload = response.json()

event = {
    "event_id": str(uuid.uuid4()),
    "ingestion_timestamp": datetime.utcnow().isoformat(),
    "source": "open_meteo",
    "payload": payload
}

producer.send("weather.hourly", event)

producer.flush()

print("Message sent successfully")