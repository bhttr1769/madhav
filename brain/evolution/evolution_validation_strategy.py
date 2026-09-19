class EvolutionValidationStrategy:
    def create(
        self,
        tasks: tuple[str, ...],
    ) -> tuple[str, ...]:
        if not isinstance(tasks, tuple):
            raise TypeError(
                "tasks must be a tuple"
            )

        for task in tasks:
            if not isinstance(task, str):
                raise TypeError(
                    "tasks must contain only strings"
                )

        if not tasks:
            return (
                "verify existing capabilities",
            )

        return (
            "run generated tests",
            "run existing engineering tests",
            "verify capability integration",
        )