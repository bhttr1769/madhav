from brain.perception.models.observation import Observation
from brain.ui.models.screen_understanding import ScreenUnderstanding


class UIObservationBuilder:
    """
    Converts existing UI screen understanding into
    perception observations.
    """

    def build(
        self,
        understanding: ScreenUnderstanding,
    ) -> frozenset[Observation]:

        if not isinstance(
            understanding,
            ScreenUnderstanding,
        ):
            raise TypeError(
                "understanding must be a ScreenUnderstanding"
            )

        observations = set()

        if understanding.application:
            observations.add(
                Observation(
                    source="ui",
                    category="application",
                    subject="screen",
                    value=understanding.application,
                )
            )

        if understanding.window_title:
            observations.add(
                Observation(
                    source="ui",
                    category="window",
                    subject="screen",
                    value=understanding.window_title,
                )
            )

        for element in understanding.elements:
            element_subject = (
                f"{element.element_type}:"
                f"{element.name}:"
                f"{element.x}:"
                f"{element.y}:"
                f"{element.width}:"
                f"{element.height}"
            )

            observations.add(
                Observation(
                    source="ui",
                    category="element",
                    subject=element_subject,
                    value=element.element_type,
                    confidence=element.confidence,
                )
            )

            if element.text is not None:
                observations.add(
                    Observation(
                        source="ui",
                        category="text",
                        subject=element_subject,
                        value=element.text,
                        confidence=element.confidence,
                    )
                )

        return frozenset(observations)