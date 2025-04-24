from fastapi import APIRouter, File, HTTPException, Header, UploadFile, status
from pydantic import BaseModel
import app.controllers.db.connector as connector
from fastapi.responses import PlainTextResponse
from app.models.data_model import GreenhouseRequest
import app.controllers.db.db_queries as db_queries
import app.kafka_module.consumer as kf
import mariadb


router = APIRouter(tags=["MariaDB"],prefix="/db")


@router.get("/initkafka")
async def get_db_info():
    kf.consume_messages()
    return PlainTextResponse("Kafka consumiendo mensajes del topic")

@router.get("/info")
async def get_db_info():
    return PlainTextResponse(connector.db_info())

@router.get("/gh/")
async def get_all_greenhouses_info(user_auth0_id: str = Header(..., alias="UserAuth")):
    return (db_queries.get_greenhouses(user_auth0_id))


@router.get("/reads/")
async def get_all_reads(user_auth0_id: str = Header(..., alias="UserAuth")):
    return (db_queries.get_reads(user_auth0_id))
   

@router.get("/gh/{id}")
async def get_greenhouse_info_by_id(id: int):
    return (db_queries.get_greenhouse(id))

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
    return (db_queries.get_reads_byid(id))
class UserCreate(BaseModel):
    email: str
    name: str
@router.post(
        "/users/",
        responses={
            200: {"description": "User already existed, returned existing record"},
            201: {"description": "New user created and returned"},
            500: {"description": "Database error"}
        },)
async def ensure_user_in_db(
    user_in: UserCreate,
    user_auth0_id: str = Header(..., alias="UserAuth")
):
    """
    Comprueba si existe un usuario con auth0_id = UserAuth header.
    Si no existe, lo crea con los datos del body.
    Devuelve el registro existente o el nuevo usuario.
    """
    try:
        conn = connector.get_con()
        cur = conn.cursor()

        # 1) Verificar si ya existe
        cur.execute(
            "SELECT id, auth0_id, email, name, created_at "
            "FROM users WHERE auth0_id = ?",
            (user_auth0_id,)
        )
        row = cur.fetchone()
        if row:
            # Usuario ya existe: devolverlo
            columns = [col[0] for col in cur.description]
            user = dict(zip(columns, row))
            conn.close()
            return user  # FastAPI devolverá status 200

        # 2) No existe: crearlo
        cur.execute(
            "INSERT INTO users (auth0_id, email, name) VALUES (?, ?, ?)",
            (user_auth0_id, user_in.email, user_in.name)
        )
        conn.commit()

        # 3) Recuperar el usuario recién creado
        last_id = cur.lastrowid
        cur.execute(
            "SELECT id, auth0_id, email, name, created_at "
            "FROM users WHERE id = ?",
            (last_id,)
        )
        row = cur.fetchone()
        columns = [col[0] for col in cur.description]
        user = dict(zip(columns, row))
        conn.close()

        # Indicamos explícitamente que fue creado
        from fastapi import Response
        return Response(
            content=user.__repr__(),
            status_code=status.HTTP_201_CREATED,
            media_type="application/json"
        )

    except mariadb.Error as e:
        print(f"DB error on ensure_user_in_db: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to ensure user in database"
        )

