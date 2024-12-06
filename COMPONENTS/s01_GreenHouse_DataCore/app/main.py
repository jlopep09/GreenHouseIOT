import asyncio
from fastapi import FastAPI
from routers.db_router import router as db_router
from fastapi.middleware.cors import CORSMiddleware
import kafka_module.consumer as kf



origins = [
    "http://web:3000",
    "http://web:8000",
]

app = FastAPI()


app.include_router(db_router)

@app.on_event("startup")
async def startup_event():
    print(f"Conectando a Kafka en kafka:9092...")
    asyncio.create_task(kf.consume_messages())



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



