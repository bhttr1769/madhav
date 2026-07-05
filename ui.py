import itertools
import sys
import threading
import time


_spinner_running = False
_spinner_thread = None
_current_message = ""


def _spin():
    global _spinner_running

    frames = itertools.cycle(
        [
            "⠋",
            "⠙",
            "⠹",
            "⠸",
            "⠼",
            "⠴",
            "⠦",
            "⠧",
            "⠇",
            "⠏"
        ]
    )

    while _spinner_running:
        frame = next(frames)

        sys.stdout.write(
            f"\r{frame} {_current_message}"
        )
        sys.stdout.flush()

        time.sleep(0.1)


def start_step(message):
    global _spinner_running
    global _spinner_thread
    global _current_message

    _current_message = message
    _spinner_running = True

    _spinner_thread = threading.Thread(
        target=_spin,
        daemon=True
    )

    _spinner_thread.start()


def finish_step():
    global _spinner_running
    global _spinner_thread
    global _current_message

    _spinner_running = False

    if _spinner_thread:
        _spinner_thread.join()

    sys.stdout.write(
        f"\r✓ {_current_message}\n"
    )
    sys.stdout.flush()


def done():
    print("✓ Done")
    time.sleep(0.2)

def smooth_print(
    text,
    delay=0.01
):
    for char in text:
        print(
            char,
            end="",
            flush=True
        )
        time.sleep(delay)

    print()

def smooth_lines(
    text,
    delay=0.05
):
    for line in text.splitlines():
        if line.strip():
            print(line)
            time.sleep(delay)