from brain.package_managers.models.build_lifecycle import (
    BuildLifecycle,
)


class BuildLifecycleDetector:
    """
    Executes registered build-lifecycle plugins.
    """

    def __init__(
        self,
        registry,
    ):

        self._registry = registry

    def detect(
        self,
        package_managers,
    ) -> set[BuildLifecycle]:

        lifecycles = set()

        for plugin in self._registry.all():

            lifecycles.update(
                plugin.detect(
                    package_managers,
                )
            )

        return lifecycles