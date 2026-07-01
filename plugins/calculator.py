
import re


def handle(user_input):
    match = re.search(
        r"calculate\s*(.+)",
        user_input,
        re.IGNORECASE
    )

    if not match:
        return False

    expression = (
        match.group(1)
        .strip()
    )

    try:
        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        print(
            f"\nMadhav: {result}\n"
        )

    except Exception:
        print(
            "\nMadhav: "
            "I couldn't calculate that.\n"
        )

    return True
