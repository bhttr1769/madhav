import json
from pathlib import Path
from datetime import datetime

MEMORY_FILE = Path("memory/memory.json")


def load_memory():
    default_memory = {
        "profile": {
            "name": "",
            "favorite_language": ""
        },
        "preferences": {},
        "projects": [],
        "memories": []
    }

    if not MEMORY_FILE.exists():
        return default_memory

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except (json.JSONDecodeError, FileNotFoundError):
        print(
            "\nWarning: memory.json is corrupted. "
            "Loading empty memory.\n"
        )
        return default_memory

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4)


def add_memory(text):
    memory = load_memory()

    text = text.strip()

    for m in memory["memories"]:
        if m["text"].lower() == text.lower():
            return

    memory["memories"].append(
        {
            "text": text,
            "timestamp": datetime.now().isoformat()
        }
    )

    save_memory(memory)


def set_name(name):
    memory = load_memory()
    memory["profile"]["name"] = name
    save_memory(memory)


def set_favorite_language(language):
    memory = load_memory()
    memory["profile"]["favorite_language"] = language
    save_memory(memory)


def get_name():
    return load_memory()["profile"]["name"]


def get_favorite_language():
    return load_memory()["profile"]["favorite_language"]


def get_memories_text():
    memory = load_memory()

    text = ""

    for m in memory["memories"]:
        text += f"- {m['text']}\n"

    return text


def get_profile():
    memory = load_memory()
    return memory["profile"]

