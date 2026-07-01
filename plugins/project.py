from pathlib import Path
import os
import re
import ast

IGNORE_FILES = {
    "main_backup.py"
}

IGNORE_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "site-packages"
}

def guess_purpose(file_name):
    name = file_name.lower()

    if "memory" in name:
        return (
            "Handles long-term memory "
            "storage and retrieval."
        )

    if "plugin" in name:
        return (
            "Loads and manages plugins."
        )

    if "command" in name:
        return (
            "Processes built-in commands."
        )

    if "main" in name:
        return (
            "Main entry point of Madhav."
        )

    if "action" in name:
        return (
            "Executes local actions "
            "such as files and commands."
        )

    return (
        "No description available."
    )

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
                root.replace(".", "")
                .count(os.sep)
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

    # ----------------------------
    # Summarize file
    # ----------------------------

    match = re.search(
        r"summarize(?: me)? (.+)",
        user_input,
        re.IGNORECASE
    )

    if match:
        file_name = (
            match.group(1)
            .strip()
        )

        if not os.path.exists(
            file_name
        ):
            print(
                "\nMadhav: File does not exist.\n"
            )
            return True

        try:
            import ast

            with open(
                file_name,
                "r",
                encoding="utf-8"
            ) as f:
                content = f.read()

            lines = (
                content.splitlines()
            )

            print(
                "\nMadhav:\n"
            )

            print(
                f"File: {file_name}"
            )

            print(
                f"Lines: {len(lines)}"
            )

            imports = []
            functions = []
            classes = []

            if file_name.endswith(".py"):
                try:
                    tree = ast.parse(
                        content
                    )

                    for node in ast.walk(
                        tree
                    ):
                        if isinstance(
                            node,
                            ast.Import
                        ):
                            for alias in node.names:
                                imports.append(
                                    alias.name
                                )

                        elif isinstance(
                            node,
                            ast.ImportFrom
                        ):
                            if node.module:
                                imports.append(
                                    node.module
                                )

                        elif isinstance(
                            node,
                            ast.FunctionDef
                        ):
                            functions.append(
                                node.name
                            )

                        elif isinstance(
                            node,
                            ast.ClassDef
                        ):
                            classes.append(
                                node.name
                            )

                except:
                    pass

            if imports:
                print(
                    "\nImports:"
                )

                for item in sorted(
                    set(imports)
                ):
                    print(
                        f"- {item}"
                    )

            if functions:
                print(
                    "\nFunctions:"
                )

                for item in functions:
                    print(
                        f"- {item}()"
                    )

            if classes:
                print(
                    "\nClasses:"
                )

                for item in classes:
                    print(
                        f"- {item}"
                    )

            if (
                not imports
                and not functions
                and not classes
            ):
                print(
                    "\nThis appears to be "
                    "a regular text file."
                )
            print(
                 "\nPurpose:"
                )
            print(
                 guess_purpose(file_name)
                )

            print()

        except Exception as e:
            print(
                f"\nMadhav: {e}\n"
            )

        return True

    # ----------------------------
    # Search code
    # ----------------------------

    match = re.search(
        r"search code for (.+)",
        user_input,
        re.IGNORECASE
    )

    if match:
        target = (
            match.group(1)
            .strip()
        )

        print("\nMadhav:\n")

        found = False

        for root, dirs, files in os.walk("."):
            dirs[:] = [
                d for d in dirs
                if d not in IGNORE_DIRS
            ]

            for file in files:
                if file in IGNORE_FILES:
                    continue

                if not file.endswith(".py"):
                    continue

                path = os.path.join(
                    root,
                    file
                )

                try:
                    with open(
                        path,
                        "r",
                        encoding="utf-8"
                    ) as f:
                        for i, line in enumerate(
                            f,
                            start=1
                        ):
                            if (
                                target.lower()
                                in line.lower()
                            ):
                                found = True
                                print(
                                    f"{path}:{i}"
                                )
                                print(
                                    f"    {line.strip()}"
                                )

                except:
                    pass

        if not found:
            print(
                "Nothing found."
            )

        print()
        return True

    # ----------------------------
    # Where is defined
    # ----------------------------

    match = re.search(
        r"where is (.+) defined",
        user_input,
        re.IGNORECASE
    )

    if match:
        target = (
            match.group(1)
            .strip()
        )

        found = False

        print("\nMadhav:\n")

        for root, dirs, files in os.walk("."):
            dirs[:] = [
                d for d in dirs
                if d not in IGNORE_DIRS
            ]

            for file in files:
                if not file.endswith(".py"):
                    continue

                if file in IGNORE_FILES:
                    continue

                path = os.path.join(
                    root,
                    file
                )

                try:
                    with open(
                        path,
                        "r",
                        encoding="utf-8"
                    ) as f:
                        for i, line in enumerate(
                            f,
                            start=1
                        ):
                            if (
                                f"def {target}"
                                in line
                                or f"class {target}"
                                in line
                            ):
                                found = True
                                print(
                                    f"{path}:{i}"
                                )
                                print(
                                    f"    {line.strip()}"
                                )

                except:
                    pass

        if not found:
            print(
                "Definition not found."
            )

        print()
        return True

    return False
