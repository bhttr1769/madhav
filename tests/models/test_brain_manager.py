from brain.manager import BrainManager


def test_brain_manager_reads_txt():

    manager = BrainManager()

    document = manager.read("tests/models/sample.txt")

    assert document.name == "sample.txt"
    assert document.extension == ".txt"
    assert "Hello Madhav!" in document.content