from kafka import KafkaProducer
import json
import time

time.sleep(30)
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_data_to_kafka(data: dict):
    topic = 'sensor_data'
    producer.send(topic, data)
    producer.flush()
