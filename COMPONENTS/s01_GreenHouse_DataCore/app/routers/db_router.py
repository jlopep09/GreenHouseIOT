from fastapi import APIRouter, File, UploadFile
import app.controllers.processor as processor
from fastapi.responses import PlainTextResponse
from app.models.data_model import GreenhouseRequest
import app.controllers.db.db_queries as db_queries

import kafka_module.consumer as kf


router = APIRouter(tags=["MariaDB"],prefix="/db")

@router.get("/initkafka")
async def get_db_info():
    kf.consume_messages()
    return PlainTextResponse(processor.get_db_info())

@router.get("/info")
async def get_db_info():
    return PlainTextResponse(processor.get_db_info())

@router.get("/gh/")
async def get_all_greenhouses_info():
    return (processor.get_all_greenhouses_info())


@router.get("/reads/")
async def get_all_reads():
    return (processor.get_all_reads())
   

@router.get("/gh/{id}")
async def get_greenhouse_info_by_id(id: int):
    return (processor.get_greenhouse_info_by_id(id))

@router.post("/gh/")
async def create_greenhouse(greenhouse: GreenhouseRequest):
    response = db_queries.create_greenhouse(
        date=greenhouse.date,
        name=greenhouse.name,
        description=greenhouse.description,
        image=greenhouse.image,
        ip=greenhouse.ip
    )
    return response
@router.post("/img")
async def post_img(image: UploadFile = File(...)):
    # Obtener el archivo de imagen y convertirlo en bytes
    image_bytes = await image.read()

    # Llamar a la función de db_queries para guardar la imagen en la base de datos
    response = db_queries.create_img(image=image_bytes)

    return response

@router.get("/reads/{id}")
async def get_reads_from_greenhouse_id(id: int):
    return (processor.get_reads_from_greenhouse_id(id))

