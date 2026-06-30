from ollama import chat

print("╔══════════════════════╗")
print("║      MADHAV v1       ║")
print("╚══════════════════════╝")
print("Type 'exit' to quit.\n")


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
        "project",
        "debug",
        "react",
        "javascript",
        "html",
        "css"
    ]

    prompt = prompt.lower()

    for word in coding_keywords:
        if word in prompt:
            return "qwen2.5-coder:3b"

    return "qwen2.5:1.5b"


SYSTEM_PROMPT = """
You are Madhav, my personal AI assistant.

You work exclusively for me.

Personality:
- Honest
- Practical
- Analytical
- Excellent at coding and problem solving
- Challenge bad ideas respectfully
- Never pretend to know something you don't

Safety Constitution:
1. Never run dangerous commands automatically.
2. Always ask before downloads or installations.
3. Log every action.
4. Never store passwords or secrets.
5. Prefer local processing.
6. Keep the user in control.
7. Explain plans before taking important actions.
8. Protect privacy and data.
9. If uncertain, ask questions.
10. Work only for the user on this machine.
"""


while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("\nGoodbye, Parth.")
        break

    model = choose_model(user_input)

    print(f"\n[Madhav is thinking using {model}...]\n")

    try:
        stream = chat(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            stream=True
        )

        print("Madhav: ", end="", flush=True)

        for chunk in stream:
            print(
                chunk["message"]["content"],
                end="",
                flush=True
            )

        print("\n")

    except Exception as e:
        print(f"\nError: {e}\n")