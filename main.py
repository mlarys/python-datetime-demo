
from datetime import datetime
from pathlib import Path

log_file = Path(__file__).resolve().parent / "execution.log"

with log_file.open("a", encoding="utf-8") as f:
    f.write(f"Executed at: {datetime.now().astimezone().isoformat()}\n")

print("Execution logged successfully.")
