import os
import re


def create_project(project_name):
    folder = os.path.join(
        "projects",
        project_name
    )

    os.makedirs(
        folder,
        exist_ok=True
    )

    files = [
        "README.md",
        "main.py",
        "requirements.txt"
    ]

    created = []

    for file in files:
        path = os.path.join(
            folder,
            file
        )

        if not os.path.exists(path):
            with open(
                path,
                "w",
                encoding="utf-8"
            ):
                pass

        created.append(file)

    return folder, created


def handle(user_input):
    match = re.search(
        r"create (?:a )?python (.+)",
        user_input,
        re.IGNORECASE
    )

    if not match:
        return False

    project_name = (
        match.group(1)
        .strip()
        .lower()
        .replace(" ", "_")
    )

    print(
        "\nMadhav:\n"
        f"I can create the project "
        f"'{project_name}'.\n"
    )

    choice = input(
        "Proceed? [Y/N]: "
    ).strip().lower()

    if choice != "y":
        print(
            "\nMadhav: Cancelled.\n"
        )
        return True

    folder, files = (
        create_project(
            project_name
        )
    )

    print(
        f"\n✓ Created {folder}"
    )

    for file in files:
        print(
            f"✓ Created {file}"
        )

    print()

    return True



