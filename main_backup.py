
from ollama import chat
from memory_manager import (
    add_memory,
    set_name,
    set_favorite_language,
    get_name,
    get_favorite_language,
    get_memories_text
)
import re

print("╔══════════════════════╗")
print("║      MADHAV v2       ║")
print("╚══════════════════════╝")
print("Type 'exit' to quit.\n")

with open("prompts/system.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

conversation = []


def choose_model(prompt):
    coding_keywords = [
        "code",
        "java",
        "python",
        "spring",
        "bug",
        "error",
        "api",
        "program",
        "algorithm",
        "sql",
        "debug",
        "react",
        "javascript",
        "html",
        "css",
        "docker",
        "git"
    ]

    prompt = prompt.lower()

    for word in coding_keywords:
        if word in prompt:
            return "qwen2.5-coder:3b"

    return "qwen2.5:1.5b"


def should_remember(text):
    text = text.lower()

    keywords = [
        "i want",
        "i like",
        "i love",
        "i prefer",
        "i am building",
        "i work on",
        "i study",
        "i use",
        "my goal",
        "my project"
    ]

    for keyword in keywords:
        if keyword in text:
            return True

    return False


while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("\nGoodbye, Parth.")
        break

    lower = user_input.lower()

    # Save name automatically
    name_match = re.search(
        r"my name is\s+(.+)",
        lower
    )

    if name_match:
        name = name_match.group(1).strip().title()
        set_name(name)

    # Save favorite language automatically
    language_match1 = re.search(
        r"my favou?rite language is\s+(.+)",
        lower
    )

    if language_match1:
        language = language_match1.group(1).strip().title()
        set_favorite_language(language)

    language_match2 = re.search(
        r"(.+)\s+is my favou?rite language",
        lower
    )

    if language_match2:
        language = language_match2.group(1).strip().title()
        set_favorite_language(language)

    # Direct memory questions
    if "who am i" in lower:
        name = get_name()

        if name:
            print(f"\nMadhav: You are {name}.\n")
        else:
            print("\nMadhav: I don't know your name yet.\n")

        continue

    if (
        "favorite language" in lower
        or "favourite language" in lower
        or "which language do i prefer" in lower
    ):
        language = get_favorite_language()

        if language:
            print(
                f"\nMadhav: Your favourite programming language is {language}.\n"
            )
        else:
            print(
                "\nMadhav: I don't know your favourite programming language yet.\n"
            )

        continue

    if "what do you know about me" in lower:
        memories = get_memories_text()

        if memories:
            print(f"\nMadhav:\n{memories}")
        else:
            print("\nMadhav: I don't know much about you yet.\n")

        continue

    # Semantic memory
    if should_remember(user_input):
        print("\nThis seems important.")
        print(f'\nRemember:\n"{user_input}"\n')

        choice = input("[Y/N]: ").strip().lower()

        if choice == "y":
            add_memory(user_input)
            print("\nMadhav: I'll remember that.\n")

    memory_context = get_memories_text()

    messages = [
        {
            "role": "system",
            "content":
                SYSTEM_PROMPT
                + "\n\nLong-term memories:\n"
                + memory_context
        }
    ]

    messages.extend(conversation)

    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    model = choose_model(user_input)

    print(f"\n[Madhav is thinking using {model}...]\n")
    print("Madhav: ", end="", flush=True)

    assistant_reply = ""

    try:
        stream = chat(
            model=model,
            messages=messages,
            stream=True
        )

        for chunk in stream:
            piece = chunk["message"]["content"]
            assistant_reply += piece
            print(piece, end="", flush=True)

        print("\n")

        conversation.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        conversation.append(
            {
                "role": "assistant",
                "content": assistant_reply
            }
        )

        if len(conversation) > 20:
            conversation = conversation[-20:]

    except Exception as e:
        print(f"\nError: {e}\n")
