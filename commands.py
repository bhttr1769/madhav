import re
from actions import (
    create_folder,
    create_file,
    read_file,
    append_to_file,
    run_command
)


def handle_commands(user_input):
    # ----------------------------
    # Create folder
    # ----------------------------

    folder_match = re.search(
        r"create (?:a )?folder(?: named)? (.+)",
        user_input,
        re.IGNORECASE
    )

    if folder_match:
        folder_name = (
            folder_match.group(1)
            .strip()
        )

        print(
            f"\nMadhav wants to create:\n"
            f"{folder_name}\n"
        )

        choice = input(
            "Proceed? [Y/N]: "
        ).strip().lower()

        if choice == "y":
            success, message = (
                create_folder(folder_name)
            )
            print(
                f"\nMadhav: {message}\n"
            )
        else:
            print(
                "\nMadhav: Action cancelled.\n"
            )

        return True

    # ----------------------------
    # Create file
    # ----------------------------

    file_match = re.search(
        r"create (?:a )?file(?: named)? (.+)",
        user_input,
        re.IGNORECASE
    )

    if file_match:
        file_name = (
            file_match.group(1)
            .strip()
        )

        print(
            f"\nMadhav wants to create:\n"
            f"{file_name}\n"
        )

        choice = input(
            "Proceed? [Y/N]: "
        ).strip().lower()

        if choice == "y":
            success, message = (
                create_file(file_name)
            )

            print(
                f"\nMadhav: {message}\n"
            )
        else:
            print(
                "\nMadhav: Action cancelled.\n"
            )

        return True

    # ----------------------------
    # Read file
    # ----------------------------

    read_match = re.search(
        r"(?:read|open)\s+(.+)",
        user_input,
        re.IGNORECASE
    )

    if read_match:
        file_name = (
            read_match.group(1)
            .strip()
        )

        success, message = (
            read_file(file_name)
        )

        if success:
            print(
                f"\nMadhav:\n{message}\n"
            )
        else:
            print(
                f"\nMadhav: {message}\n"
            )

        return True

    # ----------------------------
    # Append to file
    # ----------------------------

    append_match = re.search(
        r"append (.+) to (.+)",
        user_input,
        re.IGNORECASE
    )

    if append_match:
        text = (
            append_match.group(1)
            .strip()
        )

        file_name = (
            append_match.group(2)
            .strip()
        )

        print(
            f"\nMadhav wants to add:\n"
            f'"{text}"\n'
            f"\nto:\n{file_name}\n"
        )

        choice = input(
            "Proceed? [Y/N]: "
        ).strip().lower()

        if choice == "y":
            success, message = (
                append_to_file(
                    file_name,
                    text
                )
            )

            print(
                f"\nMadhav: {message}\n"
            )
        else:
            print(
                "\nMadhav: Action cancelled.\n"
            )

        return True

    # ----------------------------
    # Run terminal command
    # ----------------------------

    run_match = re.search(
        r"run (.+)",
        user_input,
        re.IGNORECASE
    )

    if run_match:
        command = (
            run_match.group(1)
            .strip()
        )

        print(
            f"\nMadhav wants to run:\n"
            f"{command}\n"
        )

        choice = input(
            "Proceed? [Y/N]: "
        ).strip().lower()

        if choice == "y":
            success, message = (
                run_command(command)
            )

            print(
                f"\nMadhav:\n{message}\n"
            )
        else:
            print(
                "\nMadhav: Action cancelled.\n"
            )

        return True

    return False
