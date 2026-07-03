from ollama import chat
from project_reader import (
    read_project
)


def ask_project(
    project_folder,
    question
):
    context = read_project(
        project_folder
    )

    prompt = f"""
You are an expert software engineer.

The following is an entire software project.

Project:

{context}

Question:
{question}

Answer clearly and concisely.
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

        return (
            True,
            response["message"]["content"]
        )

    except Exception as e:
        return (
            False,
            str(e)
        )