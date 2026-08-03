import math

from brain.vector.models.vector import Vector


class CosineSimilarity:
    """
    Computes cosine similarity between two vectors.
    """

    @staticmethod
    def compute(
        first: Vector,
        second: Vector,
    ) -> float:
        """
        Compute cosine similarity.
        """

        if first.dimensions != second.dimensions:
            raise ValueError(
                "Vectors must have the same dimensions."
            )

        dot_product = sum(
            a * b
            for a, b in zip(
                first.values,
                second.values,
            )
        )

        magnitude_first = math.sqrt(
            sum(
                value * value
                for value in first.values
            )
        )

        magnitude_second = math.sqrt(
            sum(
                value * value
                for value in second.values
            )
        )

        if magnitude_first == 0 or magnitude_second == 0:
            return 0.0

        return dot_product / (
            magnitude_first * magnitude_second
        )