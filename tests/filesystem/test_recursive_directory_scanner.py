def test_recursive_directory_scanner(
    tmp_path,
):

    root_file = tmp_path / "root.txt"

    subdirectory = tmp_path / "documents"

    subdirectory.mkdir()

    nested_file = (
        subdirectory
        / "nested.pdf"
    )

    root_file.write_text(
        "root"
    )

    nested_file.write_text(
        "nested"
    )

    from brain.filesystem.recursive_directory_scanner import (
        RecursiveDirectoryScanner,
    )

    scanner = (
        RecursiveDirectoryScanner()
    )

    files = scanner.scan(
        tmp_path,
    )

    assert root_file in files

    assert nested_file in files

    assert len(files) == 2