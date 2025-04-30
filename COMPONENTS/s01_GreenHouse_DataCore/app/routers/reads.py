from fastapi import APIRouter, Header
import app.controllers.db.db_queries as db_queries

router = APIRouter(tags=["MariaDB"],prefix="/db")

@router.get("/reads/")
async def get_all_reads(user_auth0_id: str = Header(..., alias="UserAuth")):
    return (db_queries.get_reads(user_auth0_id))
   

@router.get("/reads/{id}")
async def get_reads_from_greenhouse_id(id: int):
    return (db_queries.get_reads_byid(id))