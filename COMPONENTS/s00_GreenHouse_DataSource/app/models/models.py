from pydantic import BaseModel

class SensorData(BaseModel):
    tds: int
    humidity: float
    water_level: int
    temperature: float
    light_level: int
    water_temperature: float
    gh_name: str
    gh_ip: str
