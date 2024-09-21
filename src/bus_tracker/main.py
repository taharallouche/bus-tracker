from datetime import datetime
from pathlib import Path

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

LOGS_FILE_PATH = Path(__file__).parent.parent / "data" / "bus_logs.csv"


app = FastAPI(title="Bus Tracker", version="0.1.0")


class Location(BaseModel):
    latitude: float
    longitude: float


class Update(BaseModel):
    bus_id: int
    location: Location


class LogEntry(BaseModel):
    update: Update
    timestamp: datetime

    def to_row(self) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "bus_id": [self.update.bus_id],
                "latitude": [self.update.location.latitude],
                "longitude": [self.update.location.longitude],
                "timestamp": [self.timestamp],
            }
        )


@app.get("/")
async def root():
    return {"message": "Ye fatte7 ye razze9"}


@app.get("/bus/{bus_id}")
async def read_item(bus_id: int):
    logs = pd.read_csv(LOGS_FILE_PATH)
    bus_logs = logs[logs["bus_id"] == bus_id]
    latest_log = bus_logs.sort_values("timestamp").iloc[-1]
    return {
        "bus_id": bus_id,
        "latitude": latest_log["latitude"],
        "longitude": latest_log["longitude"],
    }


@app.post("/bus/{bus_id}")
async def create_item(bus_id: int, update: Update):
    logs = pd.read_csv(LOGS_FILE_PATH)
    new_entry = LogEntry(update=update, timestamp=datetime.now())

    logs = pd.concat([logs, new_entry.to_row()], ignore_index=True)
    logs.to_csv(LOGS_FILE_PATH, index=False)

    return "Thanks for the update"
