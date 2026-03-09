# Swellcheck

Automated NDBC buoy reading system that scrapes wave data, stores it in a database, exposes it via a REST API, and delivers the latest readings to users via a Telegram bot.

## What it does

- **Scraper** — Fetches NDBC spectral wave data for configured buoys every 30 minutes and writes the latest reading for each buoy into MySQL.
- **API** — FastAPI service that serves buoys and time-series readings (list, get, create, update, delete). The bot uses it to get the latest reading for buoy 51205.
- **Telegram bot** — Users send `/start` to subscribe: they receive the current buoy 51205 reading immediately, then an updated reading every 30 seconds. `/stop` unsubscribes. Other messages are echoed.

## Author

- Akila Iguchi — <akilamauihi@gmail.com>

## Implementation details

### Docker

The app runs as multiple containers orchestrated by Docker Compose: MySQL, Redis, API, Scraper (Celery worker + Beat), and the Telegram bot. Custom Dockerfiles and a single `docker-compose.yml` define the environment.

### API

FastAPI app in `api/`. Endpoints:

- **Buoys:** `GET/POST /buoys`, `GET/PATCH/DELETE /buoys/{buoy_id}`
- **Readings:** `GET/POST /readings` (optional `buoy_id` query), `GET/PATCH/DELETE /readings/{reading_id}`, `GET /buoys/{buoy_id}/readings`

Readings are returned newest-first. The bot calls `GET /buoys/51205/readings?limit=1` to get the latest reading for buoy 51205.

### Bot

Telegram bot in `bot/`. Uses the API (configurable via `API_BASE_URL`, e.g. `http://api:8000` in Docker) to fetch the latest buoy 51205 reading. On `/start` it subscribes the chat and sends the current reading, then uses a repeating job (every 30 seconds) to push updated readings to all subscribed chats. Requires `TELEGRAM_TOKEN` in `.env`.

### Scraper

Celery app in `scraper/`. Uses Redis as the broker. Celery Beat runs a job every 30 minutes that loads all buoy IDs from the database and enqueues one task per buoy. Each task fetches that buoy’s NDBC `.spec` file, parses the latest row, and inserts it into the `readings` table (with duplicate handling). NDBC data is realtime2 spectral wave data.

**Data dictionary (NDBC spec):**

| Field   | Description |
|--------|-------------|
| YY MM DD hh mm | Year, month, day, hour, minute |
| WVHT   | Significant wave height (m) — average of highest third of wave heights in the 20‑minute sample |
| SwH    | Average height of highest third of swells (m) |
| SwP    | Peak period of swells (s) |
| WWH    | Average height of highest third of wind-waves (m) |
| WWP    | Peak period of wind-waves (s) |
| SwD    | Swell direction (NESW) |
| WWD    | Wind-wave direction (NESW) |
| STEEPNESS | "VERY STEEP", "STEEP", "AVERAGE", or "SWELL" |
| APD    | Average wave period (s) over the 20‑minute period |
| MWD    | Direction of waves at dominant period (degrees) |

### init_db

Scripts or setup to initialize the MySQL database (schema and any seed data).

### Shared

`shared/` holds the MySQL connection setup and shared SQLAlchemy models/schemas (e.g. `Buoy`, `Reading`) used by both the API and the scraper.

## Project roadmap
