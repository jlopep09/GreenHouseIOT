import asyncio
import httpx
from fastapi import FastAPI
from app.routers.router_csv import router as router_csv
from fastapi.middleware.cors import CORSMiddleware
from app.kafka.producer import send_data_to_kafka

app = FastAPI()
app.include_router(router_csv)

"""
Esta función hace fetch periodico de datos a el módulo indicado, 
recoge los valores y los publica en el bus de kafka.
"""
async def fetch_and_send_data():
    url = "http://192.168.1.201/read"
    while True:
        try:
            async with httpx.AsyncClient() as client:
                print(f"Solicitando lectura...")
                response = await client.get(url)
                data = response.json()
                print(f"Respuesta JSON: {data}")
                send_data_to_kafka(data)
        except Exception as e:
            print(f"Error al hacer la petición o enviar a Kafka: {e}")
        await asyncio.sleep(30)

@app.on_event("startup")
async def startup_event():
    print(f"Iniciando suscripción de datos cada 30 segundos")
    asyncio.create_task(fetch_and_send_data())

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)