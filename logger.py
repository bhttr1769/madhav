
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("logs/actions.log")


def log_action(action):
    LOG_FILE.parent.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as f:
        f.write(
            f"[{timestamp}] {action}\n"
        )