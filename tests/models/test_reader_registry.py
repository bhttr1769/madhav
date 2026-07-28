from brain.registry.reader_registry import ReaderRegistry
from brain.io.readers.txt_reader import TXTReader


def test_reader_registry_returns_txt_reader():

    registry = ReaderRegistry()

    reader = registry.get_reader("sample.txt")

    assert isinstance(reader, TXTReader)