from fastapi import APIRouter, File,UploadFile
from fastapi.responses import PlainTextResponse
import app.kafka_module.consumer as kf
import app.controllers.db.connector as connector
import mariadb
from fastapi import HTTPException


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
    response = create_img(image=image_bytes)

    return response
def create_img(image: bytes):
    try:
        conn = connector.get_con()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO images (image) VALUES (%s)",
            (image,)  # ✅ Asegurar que es una tupla (con la coma final)
        )

        conn.commit()
        img_id = cur.lastrowid
        conn.close()
        return {"message": "Image saved successfully", "id": img_id}

    except mariadb.Error as e:
        print(f"Error de MariaDB: {e}")
        raise HTTPException(status_code=500, detail=f"Error saving image: {str(e)}")