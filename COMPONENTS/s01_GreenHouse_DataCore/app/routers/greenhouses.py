from fastapi import APIRouter, Header
import app.controllers.db.db_queries as db_queries
from pydantic import BaseModel
from typing import Optional
    
router = APIRouter(tags=["MariaDB"],prefix="/db")

class GreenhouseRequest(BaseModel):
    date: str
    name: str
    description: Optional[str] = None
    image: Optional[bytes] = None
    ip: Optional[str] = None

@router.get("/gh/")
async def get_all_greenhouses_info(user_auth0_id: str = Header(..., alias="UserAuth")):
    return (db_queries.get_greenhouses(user_auth0_id))
   

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