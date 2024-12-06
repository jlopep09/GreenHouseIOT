from pydantic import BaseModel

class SensorData(BaseModel):
    temperature: float
    humidity: float
    light_level: int
    water_level: int
    moist: int
    gh_name: str
    gh_ip: str
