import asyncio
import aiohttp
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
    timeout = aiohttp.ClientTimeout(total=10)  # Timeout de 10 segundos

    while True:
        nextTimeout = 86400
        errorCount = 0
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                print(f"Solicitando imagen...")
                async with session.get(url) as response:
                    if response.status == 200:
                        image_bytes = await response.read()
                        print("Imagen capturada. Enviando...")

                        # Enviamos como multipart/form-data
                        data = aiohttp.FormData()
                        data.add_field('file',
                                       image_bytes,
                                       filename='capture.jpg',
                                       content_type='image/jpeg')

                        async with session.post(upload_url, data=data) as upload_response:
                            if upload_response.status == 200:
                                print("Imagen enviada correctamente")
                            else:
                                print(f"Error al enviar la imagen: {upload_response.status}")
                        nextTimeout = 86400
                    else:
                        print(f"Error HTTP al capturar imagen: {response.status}")
                        nextTimeout = 300
                        errorCount += 1
        except asyncio.TimeoutError:
            print(f"Timeout al conectar con {url}. Reintentando en 5 minutos.")
            nextTimeout = 300
            errorCount += 1
        except aiohttp.ClientError as e:
            print(f"Error de cliente HTTP: {e}. Reintentando en 5 minutos.")
            nextTimeout = 300
            errorCount += 1
        except Exception as e:
            print(f"Error inesperado: {e}. Reintentando en 5 minutos.")
            nextTimeout = 300
            errorCount += 1

        if errorCount >= 10:
            nextTimeout = 83400
            errorCount = 0
            print("Se han acumulado 10 errores, se reintentará en 24h.")
        
        await asyncio.sleep(nextTimeout)

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