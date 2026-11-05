
import signal
import configparser
from pathlib import Path
from threading import Event

import pendulum

BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / "config.ini"
LOG_FILE = BASE_DIR / "execution.log"

# Read configuration
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

interval = config.getint(
    "DATETIME", "interval_seconds", fallback=10
)

timezones = [
    tz.strip()
    for tz in config.get(
        "DATETIME",
        "timezones",
        fallback="UTC,Asia/Dubai,Asia/Tokyo"
    ).split(",")
    if tz.strip()
]

if interval <= 0:
    raise ValueError("interval_seconds must be positive")

stop_event = Event()


def shutdown(signum, frame):
    print("Shutdown requested...", flush=True)
    stop_event.set()


signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)

print("Python datetime service started.", flush=True)
print(f"Interval: {interval} seconds", flush=True)
print(f"Timezones: {', '.join(timezones)}", flush=True)

while not stop_event.is_set():
    now = pendulum.now("UTC")

    message = " | ".join(
        f"{tz}: {now.in_timezone(tz).format('YYYY-MM-DD HH:mm:ss')}"
        for tz in timezones
    )

    print(message, flush=True)

    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(message + "\n")

    stop_event.wait(interval)

print("Python datetime service stopped gracefully.", flush=True)
