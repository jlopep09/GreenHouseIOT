from kafka import KafkaProducer
import json
import time

time.sleep(30)
producer = KafkaProducer(
    bootstrap_servers='vps.joselp.com:29092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_data_to_kafka(data: dict):
    print("Enviando datos por kafka")
    topic = 'sensor_data'
    producer.send(topic, data)
    producer.flush()
    print("Datos enviados")
