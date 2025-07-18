from fastapi import FastAPI
import asyncio
import aiohttp
from fastapi.middleware.cors import CORSMiddleware
from app.routers.router_csv import router as router_csv
from app.kafka.producer import send_data_to_kafka
import os

app = FastAPI()
app.include_router(router_csv)

# Token para autenticación al servicio remoto
def get_secret_token():
    return "secretgh"

async def apply_configuration_to_gh(config: dict, gh_ip: str):
    """
    Aplica la configuración recibida al invernadero vía sus endpoints HTTP.
    """
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # Luces
        lights = config.get("lights", {})
        if "on_time" in lights:
            await session.post(f"http://{gh_ip}/light/on/", data={"time": lights["on_time"]})
        if "off_time" in lights:
            await session.post(f"http://{gh_ip}/light/off/", data={"time": lights["off_time"]})
        if lights.get("force_on"):
            await session.post(f"http://{gh_ip}/light/on/", data={"now": "true"})
        if lights.get("force_off"):
            await session.post(f"http://{gh_ip}/light/off/", data={"now": "true"})

        # Oxígeno
        ox = config.get("oxygen", {})
        if "on_time" in ox:
            await session.post(f"http://{gh_ip}/oxigen/on/", data={"time": ox["on_time"]})
        if "off_time" in ox:
            await session.post(f"http://{gh_ip}/oxigen/off/", data={"time": ox["off_time"]})
        if ox.get("force_on"):
            await session.post(f"http://{gh_ip}/oxigen/on/", data={"now": "true"})
        if ox.get("force_off"):
            await session.post(f"http://{gh_ip}/oxigen/off/", data={"now": "true"})

        # Ventilador
        fan = config.get("fan", {})
        if "on_time" in fan:
            await session.post(f"http://{gh_ip}/fan/on/", data={"time": fan["on_time"]})
        if "off_time" in fan:
            await session.post(f"http://{gh_ip}/fan/off/", data={"time": fan["off_time"]})
        if fan.get("force_on"):
            await session.post(f"http://{gh_ip}/fan/on/", data={"now": "true"})
        if fan.get("force_off"):
            await session.post(f"http://{gh_ip}/fan/off/", data={"now": "true"})

        # Bomba
        pump = config.get("pump", {})
        if pump.get("force_on"):
            await session.post(f"http://{gh_ip}/pump/on/", data={"now": "true"})
        if pump.get("force_off"):
            await session.post(f"http://{gh_ip}/pump/off/", data={"now": "true"})

@app.get("/get-config/{gh_id}")
async def get_remote_config(gh_id: int):
    """
    Llama al servicio remoto de configuraciones de invernadero,
    aplica las configuraciones al dispositivo, y devuelve el JSON obtenido.
    Si la configuración al dispositivo excede 30 segundos, retorna un error de timeout.
    """
    config_url = f"https://vps.joselp.com/api/db/ghconfig/{gh_id}"
    SECRET_TOKEN = get_secret_token()
    timeout = aiohttp.ClientTimeout(total=10)

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            headers = {"Authorization": f"Bearer {SECRET_TOKEN}"}
            async with session.get(config_url, headers=headers) as response:
                response.raise_for_status()
                data = await response.json()

        # IP del invernadero local (por defecto o variable de entorno)
        gh_ip = os.getenv("GH_DEVICE_IP", "192.168.1.201")
        # Aplicar configuración con timeout global de 30s
        try:
            await asyncio.wait_for(apply_configuration_to_gh(data, gh_ip), timeout=30)
        except asyncio.TimeoutError:
            return {"error": f"Timeout al configurar invernadero en {gh_ip} (30s excedidos)"}

        return {"message": "Configuraciones obtenidas y aplicadas con éxito", "data": data}
    except aiohttp.ClientResponseError as e:
        return {"error": f"Error HTTP {e.status}: {e.message}"}
    except Exception as e:
        return {"error": str(e)}

# Tareas periódicas
async def fetch_and_send_data():
    url = "http://192.168.1.201/read"
    timeout = aiohttp.ClientTimeout(total=10)
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
    SECRET_TOKEN = get_secret_token()
    timeout = aiohttp.ClientTimeout(total=10)

    while True:
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                print(f"Solicitando imagen...")
                async with session.get(url) as response:
                    image_bytes = await response.read()
                    print("Imagen capturada. Enviando...")

                data = aiohttp.FormData()
                data.add_field('image', image_bytes, filename='capture.jpg', content_type='image/jpeg')

                headers = {'Authorization': f'Bearer {SECRET_TOKEN}'}
                async with session.post(upload_url, data=data, headers=headers) as upload_response:
                    if upload_response.status == 200:
                        print("Imagen enviada correctamente")
                    else:
                        print(f"Error al enviar la imagen codigo {upload_response.status}")
        except Exception as e:
            print(f"Error inesperado: {e}")
        await asyncio.sleep(86400)  # cada 24h

async def fetch_and_apply_config():
    """
    Cada hora obtiene la configuración del invernadero y la aplica.
    """
    gh_id = 39
    SECRET_TOKEN = get_secret_token()
    timeout = aiohttp.ClientTimeout(total=10)
    gh_ip = os.getenv("GH_DEVICE_IP", "192.168.1.201")

    while True:
        try:
            config_url = f"https://vps.joselp.com/api/db/ghconfig/{gh_id}"
            async with aiohttp.ClientSession(timeout=timeout) as session:
                headers = {"Authorization": f"Bearer {SECRET_TOKEN}"}
                async with session.get(config_url, headers=headers) as response:
                    response.raise_for_status()
                    config = await response.json()
            await asyncio.wait_for(apply_configuration_to_gh(config, gh_ip), timeout=30)
            print(f"Configuración aplicada correctamente a {gh_ip}")
        except asyncio.TimeoutError:
            print(f"Timeout al aplicar configuración a {gh_ip} (30s excedidos)")
        except Exception as e:
            print(f"Error al obtener o aplicar configuración: {e}")
        await asyncio.sleep(3600)  # cada 1h

@app.on_event("startup")
async def startup_event():
    print(f"Iniciando suscripción de datos cada 30 segundos")
    asyncio.create_task(fetch_and_send_data())
    print(f"Iniciando suscripción de imagen cada 24h")
    asyncio.create_task(fetch_and_send_img())
    print(f"Iniciando actualización de configuración cada 1h")
    asyncio.create_task(fetch_and_apply_config())

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
