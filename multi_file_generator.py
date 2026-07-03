from code_generator import (
    generate_python_code
)


def generate_todo_project():
    files = {}

    success, main_code = (
        generate_python_code(
            "todo application main file"
        )
    )

    if not success:
        return False, main_code

    success, storage_code = (
        generate_python_code(
            "todo application storage module"
        )
    )

    if not success:
        return False, storage_code

    files["main.py"] = main_code
    files["storage.py"] = storage_code

    return True, files