import asyncio
import logging
import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Load .env from project root (works when run from bot/ or project root)
load_dotenv(Path(__file__).resolve().parent.parent / ".env")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
if not TELEGRAM_TOKEN:
    raise SystemExit("TELEGRAM_TOKEN not set in .env")

# 1. Setup logging so you can see errors in the console
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def _format_reading(reading: dict) -> str:
    raw_ts = reading.get("timestamp") or "?"
    ts = raw_ts[:19].replace("T", " ") if isinstance(raw_ts, str) and len(raw_ts) >= 19 else raw_ts
    wvht = reading.get("wvht")
    swh = reading.get("swh")
    swp = reading.get("swp")
    wwh = reading.get("wwh")
    wwp = reading.get("wwp")
    swd = reading.get("swd") or "—"
    wwd = reading.get("wwd") or "—"
    apd = reading.get("apd")
    mwd = reading.get("mwd")
    parts = [
        f"Buoy 51205 — latest reading ({ts})",
        "",
        f"Wave height (WVHT): {wvht}m" if wvht is not None else None,
        f"Swell height (SWH): {swh}m" if swh is not None else None,
        f"Swell period (SWP): {swp}s" if swp is not None else None,
        f"Wind wave height (WWH): {wwh}m" if wwh is not None else None,
        f"Wind wave period (WWP): {wwp}s" if wwp is not None else None,
        f"Swell direction: {swd}",
        f"Wind wave direction: {wwd}",
    ]
    if apd is not None:
        parts.append(f"Avg wave period (APD): {apd}s")
    if mwd is not None:
        parts.append(f"Mean wave direction (MWD): {mwd}°")
    return "\n".join(p for p in parts if p is not None)


def _fetch_latest_reading() -> tuple[bool, str]:
    """Fetch latest buoy 51205 reading. Returns (ok, message)."""
    try:
        r = requests.get(
            f"{API_BASE_URL}/buoys/51205/readings",
            params={"limit": 1},
            timeout=10,
        )
        r.raise_for_status()
        readings = r.json()
    except requests.RequestException as e:
        return False, f"Could not fetch buoy data: {e!s}"
    if not readings:
        return False, "Buoy 51205 has no readings yet."
    return True, _format_reading(readings[0])


async def _broadcast_readings(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Job: send latest reading to all subscribed chats every 30s."""
    subscribed = context.bot_data.get("subscribed_chats") or set()
    if not subscribed:
        return
    ok, text = await asyncio.to_thread(_fetch_latest_reading)
    for chat_id in list(subscribed):
        try:
            await context.bot.send_message(chat_id=chat_id, text=text)
        except Exception as e:
            logging.warning("Failed to send to %s: %s", chat_id, e)


# 2. Define the /start command behavior — subscribe and send latest buoy 51205 reading
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    subscribed = context.bot_data.setdefault("subscribed_chats", set())
    subscribed.add(chat_id)
    ok, text = _fetch_latest_reading()
    await context.bot.send_message(chat_id=chat_id, text=text)
    if ok:
        await context.bot.send_message(
            chat_id=chat_id,
            text="You'll get an updated reading every 30 seconds. Send /stop to stop updates.",
        )

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Unsubscribe from 30s buoy updates."""
    chat_id = update.effective_chat.id
    subscribed = context.bot_data.get("subscribed_chats") or set()
    subscribed.discard(chat_id)
    await context.bot.send_message(chat_id=chat_id, text="Stopped buoy updates.")

# 3. Define the Echo behavior
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"You said: {update.message.text}"
    )

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.bot_data.setdefault("subscribed_chats", set())

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))

    if application.job_queue is not None:
        application.job_queue.run_repeating(_broadcast_readings, interval=30, first=30)
    else:
        logging.warning(
            "JobQueue not available (install with: pip install \"python-telegram-bot[job-queue]\"). "
            "30-second buoy updates disabled."
        )

    print("Bot is polling...")
    application.run_polling()