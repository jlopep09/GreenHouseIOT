from typing import Optional
from pydantic import BaseModel

class DataEntry(BaseModel):
    tds: int
    humidity: float
    water_level: int
    temperature: float
    light_level: int
    water_temperature: float

class GreenhouseRequest(BaseModel):
    date: str
    name: str
    description: Optional[str] = None
    image: Optional[bytes] = None
    ip: Optional[str] = None
