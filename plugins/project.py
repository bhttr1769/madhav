
import os
import re

IGNORE_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "site-packages"
}


def handle(user_input):
    lower = user_input.lower()

    # ----------------------------
    # List files
    # ----------------------------

    if (
        lower == "list files"
        or lower == "show files"
        or lower == "what files are here"
    ):
        print("\nMadhav:\n")

        for item in os.listdir("."):
            if item in IGNORE_DIRS:
                continue

            print(f"- {item}")

        print()
        return True

    # ----------------------------
    # Project tree
    # ----------------------------

    if (
        lower == "project tree"
        or lower == "show project tree"
    ):
        print("\nMadhav:\n")

        for root, dirs, files in os.walk("."):
            dirs[:] = [
                d for d in dirs
                if d not in IGNORE_DIRS
            ]

            level = (
                root.replace(
                    ".",
                    ""
                ).count(os.sep)
            )

            indent = "    " * level

            print(
                f"{indent}"
                f"{os.path.basename(root) or '.'}"
            )

            sub_indent = (
                "    "
                * (level + 1)
            )

            for file in files:
                print(
                    f"{sub_indent}"
                    f"{file}"
                )

        print()
        return True

    # ----------------------------
    # Find file
    # ----------------------------

    match = re.search(
        r"find file (.+)",
        user_input,
        re.IGNORECASE
    )

    if match:
        target = (
            match.group(1)
            .strip()
            .lower()
        )

        found = []

        for root, dirs, files in os.walk("."):
            dirs[:] = [
                d for d in dirs
                if d not in IGNORE_DIRS
            ]

            for file in files:
                if target in file.lower():
                    found.append(
                        os.path.join(
                            root,
                            file
                        )
                    )

        if found:
            print("\nMadhav:\n")

            for item in found:
                print(f"- {item}")

            print()
        else:
            print(
                "\nMadhav: "
                "No matching files found.\n"
            )

        return True

    return False
