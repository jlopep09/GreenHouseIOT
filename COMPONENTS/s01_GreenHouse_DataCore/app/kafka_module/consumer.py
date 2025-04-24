from kafka import KafkaConsumer
import json
import asyncio
import time
from app.controllers.db.db_queries import create_read
from app.controllers.detector import Detector
from app.controllers.db.db_queries import get_greenhouse_by_name

time.sleep(20)

# Define tu consumidor de Kafka fuera de la función consume_messages
consumer = KafkaConsumer(
    'sensor_data',
    bootstrap_servers='kafka:9092',
    auto_offset_reset='earliest',  # Desde el principio solo si no hay desplazamientos almacenados
    group_id='sensor_data_group',  # Identificador del grupo de consumidores
    #group_id=None,
    enable_auto_commit=True,       # Kafka almacenará automáticamente los desplazamientos
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

async def consume_messages():
    while True:
        try:
            messages = consumer.poll(timeout_ms=1000)
            for tp, msgs in messages.items():  # tp = TopicPartition
                for msg in msgs:
                    data = msg.value
                    print(f"Datos recibidos: {data}")
                    try:
                        if(Detector.checkIP(data["gh_name"], data["gh_ip"])):
                            raise Exception(detail="ERROR")   
                    except Exception as e:
                        print(f"gh ip changed! An error occurred while trying to update the gh ip. Recived read will be deleted. {e}")

                    # Procesar los datos aquí
                    bool_light = "False"
                    if(int(data["light_level"])>500):
                        bool_light = "True"
                    db_result = get_greenhouse_by_name(data["gh_name"])
                    gh_id_db = db_result["result"][0]["id"]
                    create_read(tds=data["tds"], temperature=data["temperature"], humidity=data["humidity"], light_level=bool_light, water_level=data["water_level"],water_temperature=data["water_temperature"], gh_id=int(gh_id_db))
                    

        except Exception as e:
            print(f"Error al consumir mensajes: {e}")
        await asyncio.sleep(1)  # Evitar sobrecarga de CPU





