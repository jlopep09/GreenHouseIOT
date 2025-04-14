import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse
from app.routers.db_router import router as db_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

"""import kafka_module.consumer as kf"""

SECRET_TOKEN = os.getenv("SECRET_TOKEN")


app = FastAPI()
# Middleware de autenticación
@app.middleware("http")
async def verify_authentication(request: Request, call_next):
    # Verificar si la petición viene con un token válido
    token = request.headers.get("Authorization")
    if not token or token != f"Bearer {SECRET_TOKEN}":
        detailText = "Forbidden porque me has dado un token: "+token+" y yo esperaba: Bearer "+SECRET_TOKEN
        return JSONResponse(status_code=403, content={"detail": detailText})

    # Continuar con la solicitud si es válida
    response = await call_next(request)
    return response

app.include_router(db_router)

@app.get("/health")
async def get_root():
    return PlainTextResponse("Hello, its working")

"""@app.on_event("startup")
async def startup_event():
    print(f"Conectando a Kafka en kafka:9092...")
    asyncio.create_task(kf.consume_messages())

"""

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","https://vps.joselp.com/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



