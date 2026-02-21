# Pydantic schemas for DB models
# Used to mandate input data types for functions
# Class arguments are what the database inherits

from datetime import datetime
from pydantic import BaseModel, ConfigDict


# --- Buoy (directory) ---
class BuoyBase(BaseModel):
    buoy_id: int
    location_name: str
    latitude: float | None = None
    longitude: float | None = None


class BuoyCreate(BuoyBase):
    pass


class BuoyUpdate(BaseModel):
    location_name: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class Buoy(BuoyBase):
    model_config = ConfigDict(from_attributes=True)


# --- Reading (time-series) ---
class ReadingBase(BaseModel):
    buoy_id: int
    timestamp: datetime
    wvht: float | None = None
    swh: float | None = None
    swp: float | None = None
    wwh: float | None = None
    wwp: float | None = None
    swd: str | None = None
    wwd: str | None = None
    steepness: str | None = None
    apd: float | None = None
    mwd: int | None = None


class ReadingCreate(ReadingBase):
    pass


class ReadingUpdate(BaseModel):
    timestamp: datetime | None = None
    wvht: float | None = None
    swh: float | None = None
    swp: float | None = None
    wwh: float | None = None
    wwp: float | None = None
    swd: str | None = None
    wwd: str | None = None
    steepness: str | None = None
    apd: float | None = None
    mwd: int | None = None


class Reading(ReadingBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
