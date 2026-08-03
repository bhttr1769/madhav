from brain.embedding.base_embedding import BaseEmbedding
from brain.models.document import Document


class EmbeddingPipeline:
    """
    Generates embeddings for every chunk in a document.
    """

    def __init__(self, embedding: BaseEmbedding):
        self._embedding = embedding

    def process(self, document: Document) -> Document:

        for chunk in document.chunks:
            chunk.embedding = self._embedding.embed(chunk.text)

        return document