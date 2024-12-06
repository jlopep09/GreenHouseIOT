from typing import Optional
from pydantic import BaseModel

class DataEntry(BaseModel):
    moist: int
    humidity: int
    water_level: int
    temperature: int
    light: bool

class GreenhouseRequest(BaseModel):
    date: str
    name: str
    description: Optional[str] = None
    image: Optional[bytes] = None
    ip: Optional[str] = None
