
import signal
from pathlib import Path
from threading import Event

import pendulum

log_file = Path(__file__).resolve().parent / "execution.log"
stop_event = Event()


def shutdown(signum, frame):
    print("Shutdown requested...", flush=True)
    stop_event.set()


signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)

print("Python datetime service started.", flush=True)

while not stop_event.is_set():
    now = pendulum.now("UTC")

    utc_time = now.format("YYYY-MM-DD HH:mm:ss")
    dubai_time = now.in_timezone("Asia/Dubai").format("YYYY-MM-DD HH:mm:ss")
    tokyo_time = now.in_timezone("Asia/Tokyo").format("YYYY-MM-DD HH:mm:ss")

    message = (
        f"UTC: {utc_time} | "
        f"Dubai: {dubai_time} | "
        f"Tokyo: {tokyo_time}"
    )

    print(message, flush=True)

    with log_file.open("a", encoding="utf-8") as f:
        f.write(message + "\n")

    stop_event.wait(10)

print("Python datetime service stopped gracefully.", flush=True)
