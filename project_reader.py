from pathlib import Path


def read_project(
    project_folder
):
    project_path = Path(
        project_folder
    )

    context = ""

    for file in project_path.rglob("*"):
        if (
            file.is_file()
            and file.suffix in [
                ".py",
                ".java",
                ".md",
                ".txt",
                ".xml"
            ]
        ):
            try:
                content = file.read_text(
                    encoding="utf-8"
                )

                context += (
                    f"\n===== "
                    f"{file.relative_to(project_path)} "
                    f" =====\n"
                )

                context += (
                    content
                    + "\n"
                )

            except Exception:
                pass

    return context