from fastapi import HTTPException
from sqlalchemy.orm import Session

import bus_tracker.models as models
from bus_tracker import schemas


def get_bus(db: Session, line_number: int) -> models.Bus | None:
    return db.query(models.Bus).filter(models.Bus.line_number == line_number).first()


def get_buses(db: Session, skip: int = 0, limit: int = 100) -> list[models.Bus]:
    return db.query(models.Bus).offset(skip).limit(limit).all()


def create_bus(db: Session, bus: schemas.BusCreate) -> models.Bus:
    bus = models.Bus(line_number=bus.line_number)
    db.add(bus)
    db.commit()
    db.refresh(bus)
    return bus


def get_log(db: Session, log_id: int) -> models.Log | None:
    return db.query(models.Log).filter(models.Log.id == log_id).first()


def get_logs(db: Session, skip: int = 0, limit: int = 100) -> list[models.Log]:
    return db.query(models.Log).offset(skip).limit(limit).all()


def get_logs_by_bus(
    db: Session, line_number: int, skip: int = 0, limit: int = 100
) -> list[models.Log]:
    return (
        db.query(models.Log)
        .filter(models.Log.line_number == line_number)
        .order_by(models.Log.timestamp.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_log(db: Session, log: schemas.LogCreate) -> models.Log:
    bus = get_bus(db, log.line_number)
    if not bus:
        raise HTTPException(status_code=404, detail=f"Bus {log.line_number} not found")

    db_log = models.Log(**log.model_dump())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log
