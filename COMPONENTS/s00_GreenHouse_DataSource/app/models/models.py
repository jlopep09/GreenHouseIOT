from pydantic import BaseModel

class SensorData(BaseModel):
    temperature: float
    humidity: float
    light_level: int
    water_level: int
    tds: int
    water_temperature: float
    gh_name: str
    gh_ip: str
