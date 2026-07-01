from ddgs import DDGS
import re


def handle(user_input):
    match = re.search(
        r"search (.+)",
        user_input,
        re.IGNORECASE
    )

    if not match:
        return False

    query = match.group(1).strip()

    print(f"\nMadhav: Searching for '{query}'...\n")

    try:
        with DDGS() as ddgs:
            results = list(
                ddgs.text(
                    query,
                    max_results=5
                )
            )
        if not results:
            print(
                "\nMadhav: No results found.\n"
            )
            return True

        if not results:
            print(
                "No results found.\n"
            )
            return True

        for i, result in enumerate(
            results,
            start=1
        ):
            print(
                f"{i}. {result['title']}"
            )
            print(
                f"   {result['href']}"
            )
            print()

    except Exception as e:
        print(
            f"Search failed:\n{e}\n"
            f"Details: {e}\n"
        )

    return True