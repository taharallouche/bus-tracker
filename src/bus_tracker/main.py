from typing import Annotated

from fastapi import Depends, FastAPI, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from bus_tracker import schemas
from bus_tracker.crud import create_log, get_logs_by_bus
from bus_tracker.dependencies import get_db

app = FastAPI(title="Bus Tracker", version="0.1.0")


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


@app.post("/logs", response_model=schemas.Log)
def add_log(log: schemas.LogCreate, db: Session = Depends(get_db)):
    db_log = create_log(db, log)
    return schemas.Log.model_validate(db_log)


@app.get("/bus/{line_number}/logs", response_model=list[schemas.Log])
def get_bus(
    line_number: int,
    limit: Annotated[int, Query(gt=0)] = 10,
    db: Session = Depends(get_db),
):
    logs = get_logs_by_bus(db, line_number, limit=limit)
    return [schemas.Log.model_validate(log) for log in logs]
