import re
from ollama import chat


def handle(user_input):
    match = re.search(
        r"(?:build|make)(?: me)?\s+(.+)",
        user_input,
        re.IGNORECASE
    )

    if not match:
        return False

    task = (
        match.group(1)
        .strip()
    )

    prompt = f"""
You are an expert software architect.

Create a numbered execution plan
for the following task.

Rules:
- Give exactly 5 to 8 steps.
- Keep each step under one sentence.
- Output only the numbered plan.

Task:
{task}
"""

    try:
        response = chat(
            model="qwen2.5:1.5b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        plan = (
            response["message"]
            ["content"]
        )

        print("\nMadhav:\n")
        print(f"Task: {task}\n")
        print("Plan:\n")
        print(plan)

        print(
            "\nPlanning mode only."
        )
        print(
            "Execution agent will be added later.\n"
        )

    except Exception as e:
        print(
            f"\nMadhav: {e}\n"
        )

    return True
