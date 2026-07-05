
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

def log_error(error):
    log_action(
        f"ERROR: {error}"
    )


def clear_logs():
    LOG_FILE.parent.mkdir(
        exist_ok=True
    )

    with open(
        LOG_FILE,
        "w",
        encoding="utf-8"
    ):
        pass


def get_logs():
    if not LOG_FILE.exists():
        return ""

    with open(
        LOG_FILE,
        "r",
        encoding="utf-8"
    ) as f:
        return f.read()