
from pathlib import Path
from logger import log_action
import subprocess



def create_folder(folder_name):
    path = Path(folder_name)

    if path.exists():
        return False, f"Folder already exists:\n{path}"

    path.mkdir(parents=True)

    log_action(f"Created folder: {path}")

    return True, f"Folder created successfully:\n{path}"

def create_file(file_name):
    path = Path(file_name)

    if path.exists():
        return False, f"File already exists:\n{path}"

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    path.touch()

    log_action(
        f"Created file: {path}"
    )

    return True, (
        f"File created successfully:\n{path}"
    )


def read_file(file_name):
    path = Path(file_name)

    if not path.exists():
        return False, (
            f"File does not exist:\n{path}"
        )

    if not path.is_file():
        return False, (
            f"Not a file:\n{path}"
        )

    content = path.read_text(
        encoding="utf-8"
    )

    log_action(
        f"Read file: {path}"
    )

    return True, content


def append_to_file(
    file_name,
    text
):
    path = Path(file_name)

    if not path.exists():
        return False, (
            f"File does not exist:\n{path}"
        )

    with open(
        path,
        "a",
        encoding="utf-8"
    ) as f:
        f.write(text + "\n")

    log_action(
        f"Appended to file: {path}"
    )

    return True, (
        f"Added text to:\n{path}"
    )

def run_command(command):
    blocked = [
        "del ",
        "rm ",
        "rmdir ",
        "format ",
        "shutdown ",
        "restart ",
        "taskkill ",
        "diskpart ",
        "reg delete"
    ]

    lower = command.lower()

    for word in blocked:
        if word in lower:
            return (
                False,
                "This command is blocked for safety."
            )

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        output = (
            result.stdout
            or result.stderr
            or "Command finished."
        )

        log_action(
            f"Ran command: {command}"
        )

        return True, output

    except Exception as e:
        return False, str(e)

