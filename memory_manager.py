import json
from memory_classifier import classify_memory
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
            memory = json.load(f)
            memory.setdefault("profile", {})
            memory.setdefault("preferences", {})
            memory.setdefault("projects", [])
            memory.setdefault("memories", [])
            memory["profile"].setdefault("name", "")
            memory["profile"].setdefault(
            "favorite_language",
             ""
    )
        return memory

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

    for item in memory["memories"]:
        if (
            item["text"].lower()
            == text.lower()
        ):
            return

    category, importance = (
        classify_memory(text)
    )

    memory["memories"].append(
        {
            "text": text,
            "category": category,
            "importance": importance,
            "timestamp":
                datetime.now().isoformat()
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


def get_memories_by_category(
    category
):
    memory = load_memory()

    results = []

    for item in memory["memories"]:
        if (
            item.get("category")
            == category
        ):
            results.append(
                item["text"]
            )

    return results


def get_important_memories(
    limit=5
):
    memory = load_memory()

    memories = sorted(
        memory["memories"],
        key=lambda x:
            x.get(
                "importance",
                0
            ),
        reverse=True
    )

    return memories[:limit]


def upgrade_memories():
    memory = load_memory()
    changed = False

    for item in memory["memories"]:
        if "category" not in item:
            category, importance = classify_memory(
                item["text"]
            )

            item["category"] = category
            item["importance"] = importance
            changed = True

    if changed:
        save_memory(memory)
        
       
def reclassify_memories():
    memory = load_memory()

    for item in memory["memories"]:
        category, importance = (
            classify_memory(
                item["text"]
            )
        )

        item["category"] = category
        item["importance"] = importance

    save_memory(memory)


        

