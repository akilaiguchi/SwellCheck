# Creates the object relational mapping for mysql DB=

from sqlalchemy import Column, Integer, String, Float, SmallInteger, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base


class Buoy(Base):
    __tablename__ = "buoys"

    buoy_id = Column(Integer, primary_key=True, index=True)
    location_name = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    readings = relationship("Reading", back_populates="buoy", cascade="all, delete-orphan")


class Reading(Base):
    __tablename__ = "readings"
    __table_args__ = (UniqueConstraint("buoy_id", "timestamp", name="uq_buoy_timestamp"),)

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    buoy_id = Column(Integer, ForeignKey("buoys.buoy_id", ondelete="CASCADE"), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False)
    wvht = Column(Float, nullable=True)
    swh = Column(Float, nullable=True)
    swp = Column(Float, nullable=True)
    wwh = Column(Float, nullable=True)
    wwp = Column(Float, nullable=True)
    swd = Column(String(3), nullable=True)
    wwd = Column(String(3), nullable=True)
    steepness = Column(String(10), nullable=True)
    apd = Column(Float, nullable=True)
    mwd = Column(SmallInteger, nullable=True)

    buoy = relationship("Buoy", back_populates="readings")
