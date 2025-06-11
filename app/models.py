from sqlalchemy import Column, Integer, String, Float, DateTime
from app.db import Base

class WeatherRecord(Base):
    __tablename__ = 'weather'
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    timestamp = Column(DateTime, index=True)
    temp = Column(Float)
    weather_main = Column(String)
    weather_desc = Column(String)
