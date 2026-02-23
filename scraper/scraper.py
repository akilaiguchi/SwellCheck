import os
from datetime import datetime

import requests
from celery import Celery, group
from sqlalchemy import insert

from shared.database import SessionLocal, engine, Base
from shared.models import Buoy, Reading

# Initialize connection to database
Base.metadata.create_all(bind=engine)

# Initialize celery app
app = Celery("swellcheck", broker=os.getenv("REDIS_URL"))

# Celery Beat: run scrape_job every 30 minutes
app.conf.beat_schedule = {
    "scrape-buoys-every-30min": {
        "task": "scraper.scrape_job",
        "schedule": 30 * 60,  # seconds
    },
}
app.conf.timezone = "UTC"

# NDBC uses "MM" or "999" for missing numeric values
def _safe_float(raw, missing=("MM", "999")):
    if raw is None or str(raw).strip() in missing:
        return None
    try:
        return float(raw)
    except (ValueError, TypeError):
        return None


def _safe_int(raw, missing=("MM", "999")):
    if raw is None or str(raw).strip() in missing:
        return None
    try:
        return int(float(raw))
    except (ValueError, TypeError):
        return None


def _parse_spec_timestamp(row: dict) -> datetime:
    """Build datetime from NDBC spec row (YY, MM, DD, hh, mm)."""
    yy = row.get("YY") or row.get("#YY")
    mm = row.get("MM", 1)
    dd = row.get("DD", 1)
    hh = row.get("hh", 0)
    mn = row.get("mm") or row.get("mn") or 0
    return datetime(
        int(yy) if yy is not None and str(yy).strip().isdigit() else datetime.now().year,
        _safe_int(mm) or 1,
        _safe_int(dd) or 1,
        _safe_int(hh) or 0,
        _safe_int(mn) or 0,
    )


def _spec_data_to_reading_row(buoy_id: int, data: dict) -> dict:
    """Convert one NDBC spec data row (dict) to a DB row dict. Pure, no I/O."""
    ts = _parse_spec_timestamp(data)
    return {
        "buoy_id": buoy_id,
        "timestamp": ts,
        "wvht": _safe_float(data.get("WVHT")),
        "swh": _safe_float(data.get("SwH")),
        "swp": _safe_float(data.get("SwP")),
        "wwh": _safe_float(data.get("WWH")),
        "wwp": _safe_float(data.get("WWP")),
        "swd": data.get("SwD") if str(data.get("SwD", "") or "").strip() not in ("MM", "") else None,
        "wwd": data.get("WWD") if str(data.get("WWD", "") or "").strip() not in ("MM", "") else None,
        "steepness": data.get("STEEPNESS") or None,
        "apd": _safe_float(data.get("APD")),
        "mwd": _safe_int(data.get("MWD")),
    }


def _parse_spec_response_text(text: str) -> tuple[list[str], list[dict]]:
    """Parse NDBC .spec response text into (headers, list of data dicts). Pure, no I/O."""
    lines = text.strip().split("\n")
    if not lines:
        return [], []
    headers = lines[0].split()
    data_rows = []
    for line in lines[2:]:
        if not line.strip():
            continue
        values = line.split()
        if len(values) == len(headers):
            data_rows.append(dict(zip(headers, values)))
    return headers, data_rows


# Celery worker to scrape latest buoy data
@app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 2})
def scrape_buoy(self, buoy_id: int):
    db = SessionLocal()
    try:
        response = requests.get(
            f"https://www.ndbc.noaa.gov/data/realtime2/{buoy_id}.spec", timeout=10
        )
        if response.status_code == 404:
            raise Exception(f"Buoy {buoy_id} not found")
        if response.status_code != 200:
            raise Exception(
                f"Failed to scrape buoy {buoy_id}. Status code: {response.status_code}"
            )
        _, data_rows = _parse_spec_response_text(response.text)
        if not data_rows:
            return
        row = _spec_data_to_reading_row(buoy_id, data_rows[0])
        stmt = insert(Reading).values(**row).prefix_with("IGNORE", dialect="mysql")
        db.execute(stmt)
        db.commit()
    finally:
        db.close()


# Use to initialize db with all current buoy data
# returns an array of all dictionaries of each time
def initialize_db_data(buoy_id: int):
    db = SessionLocal()
    try:
        response = requests.get(
            f"https://www.ndbc.noaa.gov/data/realtime2/{buoy_id}.spec", timeout=10
        )
        if response.status_code == 404:
            raise Exception(f"Buoy {buoy_id} not found")
        if response.status_code != 200:
            raise Exception(
                f"Failed to scrape buoy {buoy_id}. Status code: {response.status_code}"
            )
        _, data_rows = _parse_spec_response_text(response.text)
        for data in data_rows:
            row = _spec_data_to_reading_row(buoy_id, data)
            stmt = insert(Reading).values(**row).prefix_with("IGNORE", dialect="mysql")
            db.execute(stmt)
        db.commit()
        return data_rows
    finally:
        db.close()


# Celery task: get all buoy ids from DB, dispatch scrape_buoy for each concurrently
@app.task(name="scraper.scrape_job")
def scrape_job():
    db = SessionLocal()
    try:
        buoy_ids = [row[0] for row in db.query(Buoy.buoy_id).all()]
    finally:
        db.close()
    if not buoy_ids:
        return
    # Run all scrape_buoy tasks concurrently; one failure does not affect others
    group(scrape_buoy.s(bid) for bid in buoy_ids).apply_async()

