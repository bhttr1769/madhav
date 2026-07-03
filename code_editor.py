from ollama import chat
from code_generator import clean_code


def improve_code(
    file_name,
    code,
    instruction
):
    prompt = f"""
You are an expert software engineer.

File:
{file_name}

Instruction:
{instruction}

Existing code:
{code}

Rules:
- Return ONLY the updated code.
- Do not explain anything.
- Do not use markdown.
- Preserve working functionality.
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

        updated_code = clean_code(
            response["message"]["content"]
        )

        return (
            True,
            updated_code
        )

    except Exception:
        import traceback

        return (
            False,
            traceback.format_exc()
        )