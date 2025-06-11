import os
from datetime import datetime
from fastapi import Depends, Header, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

from app.models import WeatherRecord
from fastapi import FastAPI
from app.db import engine, Base, SessionLocal
load_dotenv()

# ensure tables
Base.metadata.create_all(bind=engine)

# env vars
CITY_NAME = os.getenv('CITY_NAME')
LAT = os.getenv('CITY_LAT')
LON = os.getenv('CITY_LON')
API_KEY = os.getenv('API_KEY')
EXPECTED_TOKEN = os.getenv('EXPECTED_TOKEN')

if not all([CITY_NAME, LAT, LON, API_KEY, EXPECTED_TOKEN]):
    raise RuntimeError('Missing one of required environment variables.')

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def fetch_and_store():
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={LAT}&lon={LON}&appid={API_KEY}&lang=uk"
    r = requests.get(url)
    if r.status_code != 200:
        print('Fetch error:', r.text)
        return
    data = r.json().get('current', {})
    dt = datetime.fromtimestamp(data.get('dt'))
    temp = data.get('temp')
    weather = data.get('weather', [{}])[0]
    record = WeatherRecord(
        city=CITY_NAME,
        timestamp=dt,
        temp=temp,
        weather_main=weather.get('main', ''),
        weather_desc=weather.get('description', '')
    )
    db = SessionLocal()
    db.add(record)
    db.commit()
    db.close()

@app.on_event('startup')
async def startup_event():
    scheduler = AsyncIOScheduler(timezone='Europe/Kyiv')
    scheduler.add_job(fetch_and_store, 'cron', minute=0)
    scheduler.start()

@app.get('/history')
def history(
    day: str = Query(..., regex=r'^\d{4}-\d{2}-\d{2}$'),
    x_token: str = Header(None),
    db: Session = Depends(get_db)
):
    if x_token != EXPECTED_TOKEN:
        raise HTTPException(status_code=401, detail={'error': 'Invalid token'})
    # select all records for the date, hourly
    start = datetime.fromisoformat(day + 'T00:00:00')
    end = datetime.fromisoformat(day + 'T23:59:59')
    rows = db.query(WeatherRecord).filter(
        WeatherRecord.timestamp >= start,
        WeatherRecord.timestamp <= end
    ).order_by(WeatherRecord.timestamp).all()
    result = [
        {
            'timestamp': r.timestamp.isoformat(),
            'temp': r.temp,
            'weather': r.weather_main
        }
        for r in rows
    ]
    return JSONResponse({'city': CITY_NAME, 'day': day, 'data': result})
