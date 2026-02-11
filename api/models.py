from sqlalchemy import Column, Integer, String, Float, SmallInteger, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Buoy(Base):
    __tablename__ = "buoys"

    buoy_id = Column(Integer, primary_key=True, index=True)
    location_name = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    readings = relationship("Reading", back_populates="buoy", cascade="all, delete-orphan")


class Reading(Base):
    __tablename__ = "readings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    buoy_id = Column(Integer, ForeignKey("buoys.buoy_id", ondelete="CASCADE"), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False)
    wvht = Column(Float, nullable=True)
    dpd = Column(Float, nullable=True)
    apd = Column(Float, nullable=True)
    mwd = Column(SmallInteger, nullable=True)
    wtmp = Column(Float, nullable=True)

    buoy = relationship("Buoy", back_populates="readings")
