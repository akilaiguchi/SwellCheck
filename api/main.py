from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db, engine, Base
from models import Buoy, Reading
from schemas import (
    BuoyCreate,
    BuoyUpdate,
    Buoy as BuoySchema,
    ReadingCreate,
    ReadingUpdate,
    Reading as ReadingSchema,
)

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "OpenSwell API"}


# --- Buoys (directory) ---
@app.get("/buoys", response_model=list[BuoySchema])
def list_buoys(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Buoy).offset(skip).limit(limit).all()


@app.get("/buoys/{buoy_id}", response_model=BuoySchema)
def read_buoy(buoy_id: int, db: Session = Depends(get_db)):
    buoy = db.query(Buoy).filter(Buoy.buoy_id == buoy_id).first()
    if buoy is None:
        raise HTTPException(status_code=404, detail="Buoy not found")
    return buoy


@app.post("/buoys", response_model=BuoySchema, status_code=201)
def create_buoy(payload: BuoyCreate, db: Session = Depends(get_db)):
    if db.query(Buoy).filter(Buoy.buoy_id == payload.buoy_id).first():
        raise HTTPException(status_code=400, detail="Buoy ID already exists")
    buoy = Buoy(**payload.model_dump())
    db.add(buoy)
    db.commit()
    db.refresh(buoy)
    return buoy


@app.patch("/buoys/{buoy_id}", response_model=BuoySchema)
def update_buoy(buoy_id: int, payload: BuoyUpdate, db: Session = Depends(get_db)):
    buoy = db.query(Buoy).filter(Buoy.buoy_id == buoy_id).first()
    if buoy is None:
        raise HTTPException(status_code=404, detail="Buoy not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(buoy, key, value)
    db.commit()
    db.refresh(buoy)
    return buoy


@app.delete("/buoys/{buoy_id}", status_code=204)
def delete_buoy(buoy_id: int, db: Session = Depends(get_db)):
    buoy = db.query(Buoy).filter(Buoy.buoy_id == buoy_id).first()
    if buoy is None:
        raise HTTPException(status_code=404, detail="Buoy not found")
    db.delete(buoy)
    db.commit()


# --- Readings (time-series) ---
@app.get("/readings", response_model=list[ReadingSchema])
def list_readings(
    skip: int = 0,
    limit: int = 100,
    buoy_id: int | None = Query(None, description="Filter by buoy"),
    db: Session = Depends(get_db),
):
    q = db.query(Reading)
    if buoy_id is not None:
        q = q.filter(Reading.buoy_id == buoy_id)
    return q.order_by(Reading.timestamp.desc()).offset(skip).limit(limit).all()


@app.get("/readings/{reading_id}", response_model=ReadingSchema)
def read_reading(reading_id: int, db: Session = Depends(get_db)):
    reading = db.query(Reading).filter(Reading.id == reading_id).first()
    if reading is None:
        raise HTTPException(status_code=404, detail="Reading not found")
    return reading


@app.get("/buoys/{buoy_id}/readings", response_model=list[ReadingSchema])
def list_readings_by_buoy(
    buoy_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return (
        db.query(Reading)
        .filter(Reading.buoy_id == buoy_id)
        .order_by(Reading.timestamp.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


@app.post("/readings", response_model=ReadingSchema, status_code=201)
def create_reading(payload: ReadingCreate, db: Session = Depends(get_db)):
    if db.query(Buoy).filter(Buoy.buoy_id == payload.buoy_id).first() is None:
        raise HTTPException(status_code=400, detail="Buoy not found")
    reading = Reading(**payload.model_dump())
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return reading


@app.patch("/readings/{reading_id}", response_model=ReadingSchema)
def update_reading(reading_id: int, payload: ReadingUpdate, db: Session = Depends(get_db)):
    reading = db.query(Reading).filter(Reading.id == reading_id).first()
    if reading is None:
        raise HTTPException(status_code=404, detail="Reading not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(reading, key, value)
    db.commit()
    db.refresh(reading)
    return reading


@app.delete("/readings/{reading_id}", status_code=204)
def delete_reading(reading_id: int, db: Session = Depends(get_db)):
    reading = db.query(Reading).filter(Reading.id == reading_id).first()
    if reading is None:
        raise HTTPException(status_code=404, detail="Reading not found")
    db.delete(reading)
    db.commit()
