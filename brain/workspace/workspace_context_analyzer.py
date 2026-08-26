from brain.workspace.models.workspace_context import (
    WorkspaceContext,
)

from brain.workspace.models.workspace_understanding import (
    WorkspaceUnderstanding,
)


class WorkspaceContextAnalyzer:
    """
    Interprets workspace-level context from
    synthesized workspace understanding.
    """

    def analyze(
        self,
        understanding: WorkspaceUnderstanding,
    ) -> WorkspaceContext:

        workspace_type = (
            self._detect_workspace_type(
                understanding,
            )
        )

        scale = (
            self._detect_scale(
                understanding,
            )
        )

        primary_technology = (
            self._primary(
                understanding.technologies,
            )
        )

        primary_architecture = (
            self._primary(
                understanding.architectures,
            )
        )

        confidence = (
            self._calculate_confidence(
                understanding,
            )
        )

        return WorkspaceContext(
            workspace_type=workspace_type,
            scale=scale,
            primary_technology=primary_technology,
            primary_architecture=primary_architecture,
            confidence=confidence,
        )

    def _detect_workspace_type(
        self,
        understanding: WorkspaceUnderstanding,
    ) -> str:

        if understanding.files == 0:
            return "empty"

        if (
            understanding.technologies
            or understanding.dependencies
            or understanding.architectures
        ):
            return "software_project"

        return "repository"

    def _detect_scale(
        self,
        understanding: WorkspaceUnderstanding,
    ) -> str:

        files = understanding.files

        if files == 0:
            return "empty"

        if files <= 50:
            return "small"

        if files <= 500:
            return "medium"

        return "large"

    def _primary(
        self,
        values: frozenset[str],
    ) -> str | None:

        if not values:
            return None

        return sorted(
            values,
        )[0]

    def _calculate_confidence(
        self,
        understanding: WorkspaceUnderstanding,
    ) -> float:

        evidence = 0

        if understanding.files > 0:
            evidence += 1

        if understanding.technologies:
            evidence += 1

        if understanding.dependencies:
            evidence += 1

        if understanding.architectures:
            evidence += 1

        return evidence / 4