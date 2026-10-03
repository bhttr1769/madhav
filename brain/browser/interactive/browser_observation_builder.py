from brain.browser.interactive.models.browser_observation import (
    BrowserObservation,
)
from brain.perception.models.observation import Observation


class BrowserObservationBuilder:
    """
    Converts browser observations into the generic
    perception Observation model.
    """

    def build(
        self,
        observation: BrowserObservation,
    ) -> frozenset[Observation]:

        if not isinstance(
            observation,
            BrowserObservation,
        ):
            raise TypeError(
                "observation must be a BrowserObservation"
            )

        observations = set()

        if observation.url is not None:
            observations.add(
                Observation(
                    source="browser",
                    category="url",
                    subject="page",
                    value=observation.url,
                )
            )

        if observation.title is not None:
            observations.add(
                Observation(
                    source="browser",
                    category="title",
                    subject="page",
                    value=observation.title,
                )
            )

        if observation.text is not None:
            observations.add(
                Observation(
                    source="browser",
                    category="text",
                    subject="page",
                    value=observation.text,
                )
            )

        for element in observation.elements:
            element_subject = element.selector

            observations.add(
                Observation(
                    source="browser",
                    category="element",
                    subject=element_subject,
                    value=element.element_type,
                )
            )

            if element.name is not None:
                observations.add(
                    Observation(
                        source="browser",
                        category="element_name",
                        subject=element_subject,
                        value=element.name,
                    )
                )

            if element.text is not None:
                observations.add(
                    Observation(
                        source="browser",
                        category="element_text",
                        subject=element_subject,
                        value=element.text,
                    )
                )

            observations.add(
                Observation(
                    source="browser",
                    category="interactive",
                    subject=element_subject,
                    value=str(element.interactive),
                )
            )

        return frozenset(observations)