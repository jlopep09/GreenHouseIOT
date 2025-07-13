from fastapi import APIRouter, File,UploadFile
from fastapi.responses import PlainTextResponse
import app.kafka_module.consumer as kf
import app.controllers.db.connector as connector
import mariadb
import requests
from fastapi import HTTPException, Form
import base64
from fastapi.responses import JSONResponse
from typing import Optional

router = APIRouter(tags=["MariaDB"],prefix="/db")

# Url base de tu servicio de recomendaciones
ANALYSIS_SERVICE_URL = "https://os.joselp.com/analyze-crop"

@router.get("/initkafka")
async def init_kafka():
    kf.consume_messages()
    return PlainTextResponse("Kafka consumiendo mensajes del topic")

@router.post("/img/forward-last")
async def forward_last_img(
    prompt: str = Form(...),
    temperature: Optional[float] = Form(0.3),
    max_tokens: Optional[int] = Form(1000)
):
    """
    Recupera la última imagen de la BBDD y la reenvía, junto
    con el prompt, al endpoint /analyze-crop de os.joselp.com.
    """
    # 1. Obtener última imagen
    try:
        conn = connector.get_con()
        cur = conn.cursor()
        cur.execute("SELECT id, image FROM images ORDER BY id DESC LIMIT 1")
        row = cur.fetchone()
        cur.close()
        conn.close()
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Error BBDD: {e}")

    if not row:
        return JSONResponse({"message": "No hay imágenes"}, status_code=404)

    img_id, img_bytes = row

    # 2. Preparar multipart/form-data para el servicio remoto
    data = {
        "prompt": prompt,
        "temperature": str(temperature),
        "max_tokens": str(max_tokens)
    }
    files = {
        "image": ("last.jpg", img_bytes, "application/octet-stream")
    }

    # 3. Reenvío de la petición
    try:
        resp = requests.post(
            ANALYSIS_SERVICE_URL,
            data=data,
            files=files,
            timeout=120
        )
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Error conectando al análisis: {e}")

    # 4. Propagar respuesta
    content_type = resp.headers.get("Content-Type", "")
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    # Si devuelve JSON, parseamos; si no, devolvemos texto crudo
    try:
        result = resp.json()
    except ValueError:
        return JSONResponse(content={"analysis": resp.text}, status_code=200)

    # Adjuntamos también el ID de imagen para trazabilidad
    result["image_id"] = img_id
    return result

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