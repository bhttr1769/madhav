
from pathlib import Path
from logger import log_action


def create_folder(folder_name):
    path = Path(folder_name)

    if path.exists():
        return False, f"Folder already exists:\n{path}"

    path.mkdir(parents=True)

    log_action(f"Created folder: {path}")

    return True, f"Folder created successfully:\n{path}"
