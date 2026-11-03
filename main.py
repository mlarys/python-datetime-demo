
from datetime import datetime
from pathlib import Path
from threading import Event
import signal

log_file = Path(__file__).resolve().parent / "execution.log"
stop_event = Event()

def shutdown(signum, frame):
    print("Shutdown requested...")
    stop_event.set()

signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)

print("Python service started.")

while not stop_event.is_set():
    current_time = datetime.now().astimezone().isoformat()

    # Display datetime in terminal
    print(f"Current datetime: {current_time}", flush=True)

    # Append datetime to log file
    with log_file.open("a", encoding="utf-8") as f:
        f.write(f"Executed at: {current_time}\n")

    stop_event.wait(10)

print("Python service stopped gracefully.")
