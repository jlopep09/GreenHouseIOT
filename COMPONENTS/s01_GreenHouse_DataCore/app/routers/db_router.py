from fastapi import APIRouter, File,UploadFile
from fastapi.responses import PlainTextResponse
import app.kafka_module.consumer as kf
import app.controllers.db.connector as connector
import mariadb
from fastapi import HTTPException
import base64
from fastapi.responses import JSONResponse

router = APIRouter(tags=["MariaDB"],prefix="/db")


@router.get("/initkafka")
async def init_kafka():
    kf.consume_messages()
    return PlainTextResponse("Kafka consumiendo mensajes del topic")


@router.get("/img/last")
async def get_last_img():
    try:
        conn = connector.get_con()
        cur = conn.cursor()

        # Obtener la última imagen insertada
        cur.execute("SELECT id, image FROM images ORDER BY id DESC LIMIT 1")
        row = cur.fetchone()

        cur.close()
        conn.close()

        if not row:
            return JSONResponse(content={"message": "No images found"}, status_code=404)

        img_id, img_bytes = row
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")

        # Puedes cambiar el tipo MIME si sabes que no es JPEG
        return {
            "id": img_id,
            "image_base64": img_base64,
            "mime_type": "image/jpeg"
        }

    except mariadb.Error as e:
        print(f"Error retrieving last image: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve last image")


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