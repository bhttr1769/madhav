from ollama import chat
import re


def clean_code(text):
    # Extract code block if markdown exists
    if "```" in text:
        match = re.search(
            r"```(?:python)?\n(.*?)```",
            text,
            re.DOTALL
        )

        if match:
            return (
                match.group(1)
                .strip()
            )

    # Fallback: try to find where code starts
    for keyword in [
        "import ",
        "from ",
        "def ",
        "class ",
        "if __name__"
    ]:
        index = text.find(keyword)

        if index != -1:
            return text[index:].strip()

    return text.strip()


def generate_python_code(app_name):
    prompt = f"""
Create a complete Python application called '{app_name}'.

Requirements:
- Generate a working Python program.
- Use a single file.
- Include comments where useful.
- Make the code beginner friendly.

Rules:
- Output ONLY raw Python code.
- Do not use markdown.
- Do not use ```python.
- Do not explain the code.
- Do not add any text before or after the code.
"""

    try:
        response = chat(
            model="qwen2.5-coder:3b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        code = clean_code(
            response["message"]["content"]
        )

        return (
            True,
            code
        )

    except Exception:
        import traceback

        return (
            False,
            traceback.format_exc()
        )
