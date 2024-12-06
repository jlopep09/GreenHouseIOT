from typing import Optional

import dataclasses


@dataclasses.dataclass
class Sensor_entry:
    read_id: int
    moist: int
    humidity: int
    water_level: int
    temperature: int
    light: bool
    date: str
    gh_id: int

@dataclasses.dataclass
class Greenhouse:
    gh_id: int
    date: str
    name: str
    description: Optional[str] = None
    image: Optional[bytes] = None
    ip: Optional[str] = None
