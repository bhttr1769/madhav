from ollama import chat
from memory_manager import (
    add_memory,
    set_name,
    set_favorite_language,
    get_name,
    get_favorite_language,
    get_memories_text,
    get_profile
)
from logger import log_action
from actions import create_folder
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
    user_input = input("You: ").strip()

    if user_input.lower() == "exit":
        print("\nGoodbye, Parth.")
        break

    lower = user_input.lower()

    # ----------------------------
    # Create folder command
    # ----------------------------

    folder_match = re.search(
        r"create (?:a )?folder(?: named)? (.+)",
        lower
    )

    if folder_match:
        folder_name = folder_match.group(1).strip()

        print(
            f"\nMadhav wants to create:\n"
            f"{folder_name}\n"
        )

        choice = input(
            "Proceed? [Y/N]: "
        ).strip().lower()

        if choice == "y":
            success, message = create_folder(
                folder_name
            )
            print(f"\nMadhav: {message}\n")
        else:
            print(
                "\nMadhav: Action cancelled.\n"
            )

        continue

    # ----------------------------
    # Save profile information
    # ----------------------------

    name_match = re.search(
        r".*(?:my name is|i am|i'm)\s+(.+)",
        lower,
        re.IGNORECASE
    )

    if name_match:
        name = name_match.group(1).strip().title()

        if len(name) <= 50:
            set_name(name)

    language_match1 = re.search(
        r".*my favou?rite language is\s+(.+)",
        lower,
        re.IGNORECASE
    )

    if language_match1:
        language = (
            language_match1.group(1)
            .strip()
            .title()
        )
        set_favorite_language(language)

    language_match2 = re.search(
        r"([a-zA-Z+#]+)\s+is my favou?rite language$",
        lower,
        re.IGNORECASE
    )

    if language_match2:
        language = (
            language_match2.group(1)
            .strip()
            .title()
        )

        blocked_words = [
            "what",
            "which",
            "who",
            "why",
            "how"
        ]

        if language.lower() not in blocked_words:
            set_favorite_language(language)

    # ----------------------------
    # Direct memory questions
    # ----------------------------

    if "who am i" in lower:
        name = get_name()

        if name:
            print(f"\nMadhav: You are {name}.\n")
        else:
            print(
                "\nMadhav: I don't know your name yet.\n"
            )

        continue

    if (
        "what is my favorite language" in lower
        or "what is my favourite language" in lower
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

    # ----------------------------
    # What do you know about me?
    # ----------------------------

    if (
        "know about me" in lower
        or "remember about me" in lower
        or "tell me about myself" in lower
    ):
        profile = get_profile()
        memories = get_memories_text()

        response = ""

        for key, value in profile.items():
            if value:
                label = (
                    key.replace("_", " ")
                    .title()
                )
                response += (
                    f"{label}: {value}\n"
                )

        if memories:
            response += (
                "\nOther things I remember:\n"
                + memories
            )

        if not response:
            response = (
                "I don't know much about you yet."
            )

        print(f"\nMadhav:\n{response}\n")
        continue

    # ----------------------------
    # Semantic memory
    # ----------------------------

    if should_remember(user_input):
        print("\nThis seems important.")
        print(
            f'\nRemember:\n"{user_input}"\n'
        )

        choice = input(
            "[Y/N]: "
        ).strip().lower()

        if choice == "y":
            add_memory(user_input)

            log_action(
                f"Remembered: {user_input}"
            )

            print(
                "\nMadhav: I'll remember that.\n"
            )

    # ----------------------------
    # Chat with Ollama
    # ----------------------------

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

    print(
        f"\n[Madhav is thinking using {model}...]\n"
    )
    print(
        "Madhav: ",
        end="",
        flush=True
    )

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
            print(
                piece,
                end="",
                flush=True
            )

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

    except KeyboardInterrupt:
        print("\n\nResponse cancelled.\n")
        continue

    except Exception as e:
        print(
            "\nMadhav: I couldn't connect to Ollama."
        )
        print(
            "Please make sure Ollama is running."
        )
        print(
            f"\nDetails: {e}\n"
        )
