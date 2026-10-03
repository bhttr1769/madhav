from pathlib import Path
from unittest.mock import MagicMock

from brain.manager import BrainManager
from brain.models.document import Document


def create_document() -> Document:
    return Document(
        name="test-document",
        path=Path("test-document.txt"),
        extension=".txt",
        content="test content",
        size=12,
        created_at=MagicMock(),
        modified_at=MagicMock(),
    )


def create_config():
    config = MagicMock()

    config.reader_registry.get_reader.return_value = MagicMock()
    config.parser_registry.get_parser.return_value = MagicMock()
    config.chunker_registry.get_chunker.return_value = MagicMock()

    config.embedding_pipeline.process.side_effect = (
        lambda document: document
    )

    return config


class TestBrainManagerReadIntegration:

    def test_read_gets_reader_from_reader_registry(self):
        config = create_config()

        reader = config.reader_registry.get_reader.return_value
        document = create_document()
        reader.read.return_value = document

        parser = config.parser_registry.get_parser.return_value
        parser.parse.return_value = document

        chunker = config.chunker_registry.get_chunker.return_value
        chunker.chunk.return_value = []

        manager = BrainManager(config)

        path = Path("test-document.txt")
        result = manager.read(path)

        config.reader_registry.get_reader.assert_called_once_with(path)
        assert result is document

    def test_read_reads_document_from_reader(self):
        config = create_config()

        reader = config.reader_registry.get_reader.return_value
        document = create_document()
        reader.read.return_value = document

        parser = config.parser_registry.get_parser.return_value
        parser.parse.return_value = document

        manager = BrainManager(config)

        manager.read("test-document.txt")

        reader.read.assert_called_once_with(
            Path("test-document.txt")
        )

    def test_read_passes_document_to_parser(self):
        config = create_config()

        reader = config.reader_registry.get_reader.return_value
        document = create_document()
        reader.read.return_value = document

        parser = config.parser_registry.get_parser.return_value
        parser.parse.return_value = document

        manager = BrainManager(config)

        manager.read("test-document.txt")

        parser.parse.assert_called_once_with(document)

    def test_read_gets_parser_from_parser_registry(self):
        config = create_config()

        reader = config.reader_registry.get_reader.return_value
        document = create_document()
        reader.read.return_value = document

        parser = config.parser_registry.get_parser.return_value
        parser.parse.return_value = document

        manager = BrainManager(config)

        manager.read("test-document.txt")

        config.parser_registry.get_parser.assert_called_once_with(
            Path("test-document.txt")
        )

    def test_read_chunks_parsed_document(self):
        config = create_config()

        reader = config.reader_registry.get_reader.return_value
        document = create_document()
        reader.read.return_value = document

        parser = config.parser_registry.get_parser.return_value
        parser.parse.return_value = document

        chunker = config.chunker_registry.get_chunker.return_value
        chunks = [MagicMock()]
        chunker.chunk.return_value = chunks

        manager = BrainManager(config)

        result = manager.read("test-document.txt")

        chunker.chunk.assert_called_once_with(document)
        assert result.chunks == chunks

    def test_read_processes_document_through_embedding_pipeline(self):
        config = create_config()

        reader = config.reader_registry.get_reader.return_value
        document = create_document()
        reader.read.return_value = document

        parser = config.parser_registry.get_parser.return_value
        parser.parse.return_value = document

        manager = BrainManager(config)

        result = manager.read("test-document.txt")

        config.embedding_pipeline.process.assert_called_once_with(
            document
        )
        assert result is document

    def test_read_adds_fingerprint(self):
        config = create_config()

        reader = config.reader_registry.get_reader.return_value
        document = create_document()
        reader.read.return_value = document

        parser = config.parser_registry.get_parser.return_value
        parser.parse.return_value = document

        manager = BrainManager(config)

        result = manager.read("test-document.txt")

        assert "fingerprint" in result.metadata
        assert result.metadata["fingerprint"] is not None

    def test_read_returns_document(self):
        config = create_config()

        reader = config.reader_registry.get_reader.return_value
        document = create_document()
        reader.read.return_value = document

        parser = config.parser_registry.get_parser.return_value
        parser.parse.return_value = document

        manager = BrainManager(config)

        result = manager.read("test-document.txt")

        assert isinstance(result, Document)

    def test_read_document_can_be_passed_to_learn_document(self):
        config = create_config()

        reader = config.reader_registry.get_reader.return_value
        document = create_document()
        reader.read.return_value = document

        parser = config.parser_registry.get_parser.return_value
        parser.parse.return_value = document

        manager = BrainManager(config)

        read_document = manager.read("test-document.txt")
        learned_document = manager.learn_document(read_document)

        assert learned_document is read_document
        config.memory_pipeline.ingest.assert_called_once_with(
            read_document
        )
        config.entity_pipeline.process.assert_called_once_with(
            read_document
        )
        config.relationship_pipeline.process.assert_called_once_with(
            read_document
        )

    def test_read_to_learn_document_preserves_same_document_identity(self):
        config = create_config()

        reader = config.reader_registry.get_reader.return_value
        document = create_document()
        reader.read.return_value = document

        parser = config.parser_registry.get_parser.return_value
        parser.parse.return_value = document

        manager = BrainManager(config)

        read_document = manager.read("test-document.txt")

        manager.learn_document(read_document)

        assert (
            config.memory_pipeline.ingest.call_args.args[0]
            is read_document
        )
        assert (
            config.entity_pipeline.process.call_args.args[0]
            is read_document
        )
        assert (
            config.relationship_pipeline.process.call_args.args[0]
            is read_document
        )