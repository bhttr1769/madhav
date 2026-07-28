from brain.manager import BrainManager


def test_brain_manager_reads_and_parses_txt():

    manager = BrainManager()

    document = manager.read("tests/models/sample.txt")

    assert document.name == "sample.txt"
    assert document.extension == ".txt"
    assert "Hello Madhav!" in document.content

    assert document.metadata["word_count"] == 7
    assert document.metadata["line_count"] == 2
    assert document.metadata["reading_time_minutes"] == 1