from brain.capabilities.models.capability_composition import (
    CapabilityComposition,
)
from brain.capabilities.models.capability_reliability_assessment import (
    CapabilityReliabilityAssessment,
)
from brain.capabilities.models.capability_reliability_composition import (
    CapabilityReliabilityComposition,
)


class CapabilityReliabilityComposer:
    def compose(
        self,
        composition: CapabilityComposition,
        assessments: tuple[
            CapabilityReliabilityAssessment,
            ...,
        ],
    ) -> CapabilityReliabilityComposition:
        if not isinstance(
            composition,
            CapabilityComposition,
        ):
            raise TypeError(
                "composition must be a CapabilityComposition"
            )

        if not isinstance(assessments, tuple):
            raise TypeError(
                "assessments must be a tuple"
            )

        capability_ids = tuple(
            capability.id
            for capability in composition.capabilities
        )

        if len(set(capability_ids)) != len(capability_ids):
            raise ValueError(
                "composition contains duplicate capabilities"
            )

        assessment_ids = tuple(
            assessment.capability_id
            for assessment in assessments
        )

        if len(set(assessment_ids)) != len(assessment_ids):
            raise ValueError(
                "assessments contain duplicate capabilities"
            )

        if set(assessment_ids) != set(capability_ids):
            raise ValueError(
                "assessments must match composition capabilities"
            )

        return CapabilityReliabilityComposition(
            composition=composition,
            assessments=assessments,
        )