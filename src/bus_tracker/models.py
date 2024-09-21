from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from bus_tracker.database import Base


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    line_number = Column(Integer, ForeignKey("buses.line_number"), nullable=False)
    location_lat = Column(Float, nullable=False)
    location_lon = Column(Float, nullable=False)
    timestamp = Column(DateTime)

    bus = relationship("Bus", back_populates="logs")


class Buses(Base):
    __tablename__ = "buses"

    line_number = Column(Integer, primary_key=True)

    logs = relationship("Log", order_by=Log.id, back_populates="bus")
