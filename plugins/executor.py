import os
import re
from pathlib import Path

def copy_template(
    template_name,
    project_name,
    destination
):
    template_dir = (
        Path("templates")
        / template_name
    )

    for file in template_dir.iterdir():
        content = (
            file.read_text(
                encoding="utf-8"
            )
        )

        content = content.replace(
            "{{PROJECT_NAME}}",
            project_name
        )

        target = (
            Path(destination)
            / file.name
        )

        target.write_text(
            content,
            encoding="utf-8"
        )


def create_project(project_name):
    folder = os.path.join(
        "projects",
        project_name
    )

    os.makedirs(
        folder,
        exist_ok=True
    )

    copy_template(
        "python_app",
        project_name,
        folder
    )

    created = [
        "README.md",
        "main.py",
        "requirements.txt"
    ]

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



