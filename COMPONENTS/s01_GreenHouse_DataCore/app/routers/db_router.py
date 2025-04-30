from fastapi import APIRouter, File,UploadFile
from fastapi.responses import PlainTextResponse
import app.controllers.db.db_queries as db_queries
import app.kafka_module.consumer as kf


router = APIRouter(tags=["MariaDB"],prefix="/db")


@router.get("/initkafka")
async def init_kafka():
    kf.consume_messages()
    return PlainTextResponse("Kafka consumiendo mensajes del topic")

@router.post("/img")
async def post_img(image: UploadFile = File(...)):
    # Obtener el archivo de imagen y convertirlo en bytes
    image_bytes = await image.read()

    # Llamar a la función de db_queries para guardar la imagen en la base de datos
    response = db_queries.create_img(image=image_bytes)

    return response
