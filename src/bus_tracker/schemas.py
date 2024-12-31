from datetime import datetime

from pydantic import BaseModel


class BusBase(BaseModel):
    line_number: int


class BusCreate(BusBase):
    pass


class Bus(BusBase):
    class Config:
        orm_mode = True
        from_attributes = True


class LogBase(BaseModel):
    line_number: int
    location_lat: float
    location_lon: float


class LogCreate(LogBase):
    pass


class Log(LogBase):
    timestamp: datetime

    class Config:
        orm_mode = True
        from_attributes = True
