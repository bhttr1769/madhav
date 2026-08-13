from brain.vector.models.vector_record import VectorRecord


class VectorStore:
    """
    In-memory storage for vector records.
    """

    def __init__(self):
        self._records: dict[str, VectorRecord] = {}

    def add(self, record: VectorRecord) -> None:
        """
        Store a vector record.
        """
        self._records[record.id] = record

    def get(self, record_id: str) -> VectorRecord | None:
        """
        Retrieve a vector record.
        """
        return self._records.get(record_id)

    def remove(self, record_id: str) -> None:
        """
        Remove a vector record.
        """
        self._records.pop(record_id, None)

    def exists(self, record_id: str) -> bool:
        """
        Check whether a record exists.
        """
        return record_id in self._records

    def all(self) -> list[VectorRecord]:
        """
        Return all stored records.
        """
        return list(self._records.values())

    def count(self) -> int:
        """
        Return the number of stored records.
        """
        return len(self._records)

    def clear(self) -> None:
        """
        Remove all stored records.
        """
        self._records.clear()

    def has_document(
        self,
        document_id: str,
    ) -> bool:
        """
        Check whether vectors for a document
        already exist.
        """

        return any(
            record.document_id == document_id
            for record in self._records.values()
        )

    def remove_document(
        self,
        document_id: str,
    ) -> None:
        """
        Remove all vectors belonging
        to a document.
        """

        ids = [
            record.id
            for record in self._records.values()
            if record.document_id == document_id
        ]

        for record_id in ids:
            self.remove(record_id)