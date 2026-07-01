import re
import requests
from bs4 import BeautifulSoup
from ollama import chat


def handle(user_input):
    match = re.search(
        r"(?:read|summarize)\s+(https?://.+)",
        user_input,
        re.IGNORECASE
    )

    if not match:
        return False

    url = match.group(1).strip()

    print(
        f"\nMadhav: Reading {url}...\n"
    )

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent":
                "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        title = (
            soup.title.string.strip()
            if soup.title
            and soup.title.string
            else "No title"
        )

        paragraphs = []

        for p in soup.find_all("p"):
            text = p.get_text(
                " ",
                strip=True
            )

            if len(text) > 40:
                paragraphs.append(
                    text
                )

        print(
            f"Title: {title}"
        )

        print(
            f"URL: {url}\n"
        )

        if not paragraphs:
            print(
                "No readable content found.\n"
            )
            return True

        article = "\n\n".join(
            paragraphs[:15]
        )

        if len(article) > 4000:
            article = article[:4000]

        prompt = f"""
You are a documentation summarizer.

Respond ONLY in this format:

Summary:
<2-4 sentences>

Key Points:
- point 1
- point 2
- point 3
- point 4

Article:

{article}
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

            summary = (
                response["message"]
                ["content"]
            )

            print(summary)
            print()

        except Exception:
            print(
                "AI summarization failed."
            )
            print(
                "\nArticle Preview:\n"
            )
            print(
                article[:1500]
            )
            print()

    except Exception as e:
        print(
            f"\nMadhav: {e}\n"
        )

    return True
