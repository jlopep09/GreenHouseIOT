# app/kafka_module/consumer.py

import os
import json
import asyncio
import time

from kafka import KafkaConsumer
from app.controllers.db.db_queries import create_read, get_greenhouse_by_name
from app.controllers.detector import Detector

# Delay inicial para asegurar que Kafka esté listo en producción
time.sleep(20)

def _build_consumer():
    return KafkaConsumer(
        'sensor_data',
        bootstrap_servers='kafka:9092',
        auto_offset_reset='earliest',
        group_id='sensor_data_group',
        enable_auto_commit=True,
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )

# Si estamos en entorno de tests, no creamos el consumidor real
if os.getenv("TESTING"):
    consumer = None
else:
    consumer = _build_consumer()


def get_consumer():
    """
    Devuelve el KafkaConsumer en producción,
    y None si estamos en TESTING para evitar errores de conexión.
    """
    return consumer


async def consume_messages():
    """
    Bucle asíncrono que consume mensajes solo si `consumer` está inicializado.
    En TESTING, get_consumer() retorna None y nunca entrará en el bucle real.
    """
    cons = get_consumer()
    if cons is None:
        print("Kafka consumer deshabilitado (TESTING active). No se consumirán mensajes.")
        return

    while True:
        try:
            messages = cons.poll(timeout_ms=1000)
            for tp, msgs in messages.items():
                for msg in msgs:
                    data = msg.value
                    print(f"Datos recibidos: {data}")
                    try:
                        if Detector.checkIP(data["gh_name"], data["gh_ip"], data["sync_code"]):
                            raise Exception(detail="ERROR")
                    except Exception as e:
                        print(f"gh ip changed! {e}")

                    # Procesar los datos y grabar en BD
                    bool_light = "True" if int(data["light_level"]) > 500 else "False"
                    db_result = get_greenhouse_by_name(data["gh_name"])
                    gh_id_db = db_result["result"][0]["id"]
                    create_read(
                        tds=data["tds"],
                        temperature=data["temperature"],
                        humidity=data["humidity"],
                        light_level=bool_light,
                        water_level=data["water_level"],
                        water_temperature=data["water_temperature"],
                        gh_id=int(gh_id_db)
                    )

        except Exception as e:
            print(f"Error al consumir mensajes: {e}")

        await asyncio.sleep(1)
