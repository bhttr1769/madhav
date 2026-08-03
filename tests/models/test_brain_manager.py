from brain.manager import BrainManager
from tests.utils.testing_factory import TestBrainFactory

def test_brain_manager_reads_and_parses_txt():

    manager = TestBrainFactory.create()

    document = manager.read("tests/models/sample.txt")

    assert document.name == "sample.txt"
    assert document.extension == ".txt"
    assert "Hello Madhav!" in document.content

    assert document.metadata["word_count"] == 7
    assert document.metadata["line_count"] == 2
    assert document.metadata["reading_time_minutes"] == 1
    
#Verify chunking
    assert len(document.chunks) > 0
    assert "Hello Madhav!" in document.chunks[0].text