from brain.engineering.tasks.models.task import Task


class EvolutionTaskSequencer:
    def sequence(
        self,
        tasks: tuple[Task, ...],
    ) -> tuple[Task, ...]:
        if not isinstance(tasks, tuple):
            raise TypeError(
                "tasks must be a tuple"
            )

        for task in tasks:
            if not isinstance(task, Task):
                raise TypeError(
                    "tasks must contain only Task instances"
                )

        return tasks