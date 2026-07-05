import re
import session_memory as memory
import command_history
import logger
import undo_manager
import os
import shutil
import plugin_manager
import terminal_ui as tui
from task_state import (
    get_state
)
from actions import (
    create_folder,
    create_file,
    read_file,
    append_to_file,
    run_command
)


def handle_commands(user_input):

    memory.set(
        "last_command",
        user_input
    )
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
        if success:
            undo_manager.set_action(
            "create_folder",
            folder_name
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
        if success:
            undo_manager.set_action(
            "create_file",
            file_name
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

        if (
            file_name.startswith("http://")
            or file_name.startswith("https://")
        ):
            return False
        
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

            old_content = ""

            if os.path.exists(file_name):
                with open(
                    file_name,
                    "r",
                    encoding="utf-8"
                ) as f:
                    old_content = f.read()

            success, message = (
                append_to_file(
                    file_name,
                    text
                )
            )

            if success:
                undo_manager.set_action(
                    "append",
                    {
                        "file": file_name,
                        "content": old_content
                    }
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
            tui.success(
                message
            )

            tui.blank()
        else:
            print(
                "\nMadhav: Action cancelled.\n"
            )

        return True

    # ----------------------------
    # status
    # ----------------------------

    if user_input.lower() == "status":

        tui.section(
            "System"
        )

        tui.info(
            f"State : {get_state()}"
    )

        tui.blank()
        return True

    # ----------------------------
    # memory commands
    # ----------------------------

    
    if user_input.lower() == "memory":
        tui.section(
            "Memory"
        )

        print(
        memory.all()
        )

        tui.blank()
        return True

    if user_input.lower() == "clear memory":
        memory.clear()

        print(
            "\nMadhav:\n"
            "Memory cleared.\n"
        )

        return True

    if user_input.lower() == "history":
        history = command_history.get()

        print("\nMadhav:")

        if history:
            for i, command in enumerate(
                history,
                start=1
            ):
                print(
                    f"{i}. {command}"
                )
        else:
            print(
                "No command history."
            )

        print()

        return True


    if user_input.lower() == "clear history":
        command_history.clear()

        print(
            "\nMadhav:\n"
            "History cleared.\n"
        )

        return True

    if user_input.lower() == "undo":
        action = undo_manager.get_action()

        if not action:
            print(
                "\nMadhav:\n"
                "Nothing to undo.\n"
            )
            return True

        action_type = action["type"]
        data = action["data"]

        try:
            if action_type == "create_file":
                if os.path.exists(data):
                    os.remove(data)

            elif action_type == "create_folder":
                if os.path.exists(data):
                    shutil.rmtree(data)

            elif action_type == "append":
                with open(
                    data["file"],
                    "w",
                    encoding="utf-8"
                ) as f:
                    f.write(
                        data["content"]
                    )

            undo_manager.clear()

            print(
                "\nMadhav:\n"
                "Undo successful.\n"
            )

        except Exception as e:
            print(
                f"\nMadhav:\n"
                f"Undo failed:\n{e}\n"
            )

        return True
   
    if user_input.lower() == "logs":
        logs = logger.get_logs()

        if not logs:
            logs = "No logs found."


        tui.section(
            "Logs"
        )

        print(logs)

        tui.blank()

        return True
    
    if user_input.lower() == "clear logs":
        logger.clear_logs()

        print(
            "\nMadhav:\n"
            "Logs cleared.\n"
        )

        return True
    
    if user_input.lower() == "plugins":
        plugins = (
            plugin_manager.get_plugins()
        )

        tui.section(
            "Plugins"
        )

        for(
            name,
            enabled
        ) in plugins.items():

            status = (
                "✓"
                if enabled
                else "✗"
            )

        print(
            f"{status} {name}"
        )

        tui.blank()

        return True

    enable_match = re.search(
        r"enable (.+)",
        user_input,
        re.IGNORECASE
        )

    if enable_match:
        plugin_name = (
            enable_match.group(1)
            .strip()
        )

        success = (
            plugin_manager.enable_plugin(
                plugin_name
            )
        )

        if success:
            print(
                f"\nMadhav:\n"
                f"Enabled {plugin_name}\n"
            )
        else:
            print(
                "\nMadhav:\n"
                "Plugin not found.\n"
            )

        return True

    disable_match = re.search(
        r"disable (.+)",
        user_input,
        re.IGNORECASE
    )

    if disable_match:
        plugin_name = (
            disable_match.group(1)
            .strip()
        )

        success = (
            plugin_manager.disable_plugin(
                plugin_name
            )
        )

        if success:
            print(
                f"\nMadhav:\n"
                f"Disabled {plugin_name}\n"
            )
        else:
            print(
                "\nMadhav:\n"
                "Plugin not found.\n"
            )

        return True

    return False
