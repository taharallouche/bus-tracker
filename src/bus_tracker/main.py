from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from bus_tracker import schemas
from bus_tracker.crud import create_log, get_bus, get_buses, get_logs_by_bus
from bus_tracker.dependencies import get_db

# Run it with:
# uvicorn src.bus_tracker.main:app  --reload --host 0.0.0.0 --port 8000

app = FastAPI(title="Bus Tracker", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Welcome to My Bus Tracker</title>
        </head>
        <body>
            <h1>Welcome to My Bus Tracker</h1>
            <p>This is a simple FastAPI application.</p>
        </body>
    </html>
    """


@app.post("/logs", response_model=schemas.Log, status_code=status.HTTP_201_CREATED)
def add_log(log: schemas.LogCreate, db: Session = Depends(get_db)):
    bus = get_bus(db, log.line_number)
    if bus is None:
        raise HTTPException(status_code=404, detail=f"Bus {log.line_number} not found")
    db_log = create_log(db, log)
    return schemas.Log.model_validate(db_log)


@app.get("/bus/{line_number}/logs", response_model=list[schemas.Log])
def get_bus_logs(
    line_number: int,
    limit: Annotated[int, Query(gt=0)] = 10,
    db: Session = Depends(get_db),
):
    logs = get_logs_by_bus(db, line_number, limit=limit)
    return [schemas.Log.model_validate(log) for log in logs]


@app.get("/buses", response_model=list[schemas.Bus])
def get_all_buses(db: Session = Depends(get_db)):
    buses = get_buses(db)
    return [schemas.Bus.model_validate(bus) for bus in buses]
