from collections import defaultdict

from brain.evolution.models.evolution_experience import (
    EvolutionExperience,
)

from brain.evolution.models.evolution_history import (
    EvolutionHistory,
)

from brain.evolution.models.evolution_improvement_category import (
    EvolutionImprovementCategory,
)

from brain.evolution.models.evolution_improvement_observation import (
    EvolutionImprovementObservation,
)


class EvolutionImprovementAnalyzer:
    """
    Analyzes evolution history and experience for
    repeated, explicitly classifiable improvement
    evidence.
    """

    _CATEGORY_MARKERS = (
        (
            "requirement understanding:",
            EvolutionImprovementCategory.REQUIREMENT_UNDERSTANDING,
        ),
        (
            "task decomposition:",
            EvolutionImprovementCategory.TASK_DECOMPOSITION,
        ),
        (
            "system design:",
            EvolutionImprovementCategory.SYSTEM_DESIGN,
        ),
        (
            "engineering planning:",
            EvolutionImprovementCategory.ENGINEERING_PLANNING,
        ),
        (
            "code generation:",
            EvolutionImprovementCategory.CODE_GENERATION,
        ),
        (
            "test generation:",
            EvolutionImprovementCategory.TEST_GENERATION,
        ),
        (
            "verification:",
            EvolutionImprovementCategory.VERIFICATION,
        ),
        (
            "debugging:",
            EvolutionImprovementCategory.DEBUGGING,
        ),
        (
            "refactoring:",
            EvolutionImprovementCategory.REFACTORING,
        ),
        (
            "capability discovery:",
            EvolutionImprovementCategory.CAPABILITY_DISCOVERY,
        ),
        (
            "capability integration:",
            EvolutionImprovementCategory.CAPABILITY_INTEGRATION,
        ),
        (
            "dependency management:",
            EvolutionImprovementCategory.DEPENDENCY_MANAGEMENT,
        ),
        (
            "safety:",
            EvolutionImprovementCategory.SAFETY,
        ),
        (
            "recovery:",
            EvolutionImprovementCategory.RECOVERY,
        ),
        (
            "orchestration:",
            EvolutionImprovementCategory.ORCHESTRATION,
        ),
    )

    def __init__(
        self,
        minimum_occurrences: int = 2,
    ):
        if not isinstance(
            minimum_occurrences,
            int,
        ):
            raise TypeError(
                "minimum_occurrences must be an integer"
            )

        if minimum_occurrences < 2:
            raise ValueError(
                "minimum_occurrences must be at least 2"
            )

        self._minimum_occurrences = (
            minimum_occurrences
        )

    def analyze(
        self,
        histories: tuple[
            EvolutionHistory,
            ...
        ],
        experiences: tuple[
            EvolutionExperience,
            ...
        ],
    ) -> tuple[
        EvolutionImprovementObservation,
        ...,
    ]:
        if not isinstance(
            histories,
            tuple,
        ):
            raise TypeError(
                "histories must be a tuple"
            )

        if not isinstance(
            experiences,
            tuple,
        ):
            raise TypeError(
                "experiences must be a tuple"
            )

        for history in histories:
            if not isinstance(
                history,
                EvolutionHistory,
            ):
                raise TypeError(
                    "histories must contain only "
                    "EvolutionHistory instances"
                )

        for experience in experiences:
            if not isinstance(
                experience,
                EvolutionExperience,
            ):
                raise TypeError(
                    "experiences must contain only "
                    "EvolutionExperience instances"
                )

        history_by_id = {
            history.evolution_id: history
            for history in histories
        }

        evidence = defaultdict(
            list
        )

        for experience in experiences:
            if experience.outcome == "success":
                continue

            category = (
                self._classify_task(
                    experience.task_description
                )
            )

            if category is None:
                continue

            evidence[
                (
                    category,
                    experience.task_description,
                    experience.lesson,
                )
            ].append(
                experience.evolution_id
            )

        observations = []

        for (
            category,
            task_description,
            lesson,
        ), evolution_ids in evidence.items():
            unique_evolution_ids = tuple(
                dict.fromkeys(
                    evolution_ids
                )
            )

            if len(
                unique_evolution_ids
            ) < self._minimum_occurrences:
                continue

            existing_history_ids = tuple(
                evolution_id
                for evolution_id
                in unique_evolution_ids
                if evolution_id
                in history_by_id
            )

            if len(
                existing_history_ids
            ) < self._minimum_occurrences:
                continue

            observations.append(
                EvolutionImprovementObservation(
                    category=category,
                    description=(
                        "Repeated unsuccessful "
                        f"experience in {task_description}: "
                        f"{lesson}"
                    ),
                    evolution_ids=(
                        existing_history_ids
                    ),
                    occurrence_count=len(
                        existing_history_ids
                    ),
                )
            )

        return tuple(
            observations
        )

    def _classify_task(
        self,
        task_description: str,
    ):
        if not isinstance(
            task_description,
            str,
        ):
            return None

        normalized = (
            task_description
            .strip()
            .lower()
        )

        for marker, category in (
            self._CATEGORY_MARKERS
        ):
            if normalized.startswith(
                marker
            ):
                return category

        return None