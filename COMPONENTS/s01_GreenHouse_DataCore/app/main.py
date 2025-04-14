from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from app.routers.db_router import router as db_router
from fastapi.middleware.cors import CORSMiddleware

"""import kafka_module.consumer as kf"""



app = FastAPI()
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



