
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


def detect_template(user_input):
    lower = user_input.lower()

    if "flask" in lower:
        return "flask_api"

    return "python_app"


def get_project_folder(
    project_name
):
    folder = os.path.join(
        "projects",
        project_name
    )

    if not os.path.exists(folder):
        return folder

    counter = 1

    while True:
        new_folder = os.path.join(
            "projects",
            f"{project_name}_{counter}"
        )

        if not os.path.exists(
            new_folder
        ):
            return new_folder

        counter += 1


def create_project(
    project_name,
    template
):
    folder = get_project_folder(
        project_name
    )

    os.makedirs(
        folder,
        exist_ok=True
    )

    copy_template(
        template,
        project_name,
        folder
    )

    created = []

    for file in os.listdir(folder):
        created.append(file)

    return folder, created


def handle(user_input):
    match = re.search(
        r"create (.+)",
        user_input,
        re.IGNORECASE
    )

    if not match:
        return False

    request = (
        match.group(1)
        .strip()
    )

    template = detect_template(
        user_input
    )

    project_name = request.lower()

    words_to_remove = {
        "python",
        "flask",
        "spring",
        "boot",
        "react",
        "app",
        "api",
        "a"
    }

    words = []

    for word in project_name.split():
        if word not in words_to_remove:
            words.append(word)

    project_name = "_".join(words)

    if not project_name:
        project_name = "my_project"

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
            project_name,
            template
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
