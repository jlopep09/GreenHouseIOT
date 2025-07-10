import asyncio
import aiohttp
from fastapi import FastAPI
from app.routers.router_csv import router as router_csv
from fastapi.middleware.cors import CORSMiddleware
from app.kafka.producer import send_data_to_kafka
import os

app = FastAPI()
app.include_router(router_csv)

"""
Esta función hace fetch periodico de datos a el módulo indicado, 
recoge los valores y los publica en el bus de kafka.
"""
async def fetch_and_send_data():
    url = "http://192.168.1.201/read"
    timeout = aiohttp.ClientTimeout(total=10)  # Timeout de 10 segundos
    
    while True:
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                print(f"Solicitando lectura...")
                async with session.get(url) as response:
                    data = await response.json()
                    print(f"Respuesta JSON: {data}")
                    send_data_to_kafka(data)
        except asyncio.TimeoutError:
            print(f"Timeout al conectar con {url}. La API podría estar inactiva.")
        except aiohttp.ClientError as e:
            print(f"Error de cliente HTTP: {e}")
        except Exception as e:
            print(f"Error al hacer la petición o enviar a Kafka: {e}")
        
        await asyncio.sleep(30)
async def fetch_and_send_img():
    url = "http://192.168.1.202/capture"
    upload_url = "https://vps.joselp.com/api/db/img"
    SECRET_TOKEN = "secretgh"  # <-- lee el token aquí
    timeout = aiohttp.ClientTimeout(total=10)

    while True:
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                # Captura la imagen
                print(f"Solicitando imagen...")
                async with session.get(url) as response:
                    image_bytes = await response.read()
                    print("Imagen capturada. Enviando...")
                
                # Prepara multipart/form-data
                data = aiohttp.FormData()
                data.add_field('image',
                               image_bytes,
                               filename='capture.jpg',
                               content_type='image/jpeg')

                # Añade la cabecera Authorization
                headers = {
                    'Authorization': f'Bearer {SECRET_TOKEN}'
                }

                # Envía la imagen
                async with session.post(upload_url, data=data, headers=headers) as upload_response:
                    if upload_response.status == 200:
                        print("Imagen enviada correctamente")
                    else:
                        print(f"Error al enviar la imagen codigo {upload_response.status}: {upload_response} ")
                        print(f"Los datos enviados fueron {data}")
        except Exception as e:
            print(f"Error inesperado: {e}")
        
        await asyncio.sleep(86400)
@app.on_event("startup")
async def startup_event():
    print(f"Iniciando suscripción de datos cada 30 segundos")
    asyncio.create_task(fetch_and_send_data())
    print(f"Iniciando suscripción de imagen cada 24h")
    asyncio.create_task(fetch_and_send_img())

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)