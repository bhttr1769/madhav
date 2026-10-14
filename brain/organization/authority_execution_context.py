from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Iterator


@dataclass(frozen=True)
class AuthorityExecutionContext:
    """Trusted identity propagated through one agent execution."""

    agent_id: str
    organization_id: str | None

    def __post_init__(self) -> None:
        if not isinstance(self.agent_id, str) or not self.agent_id.strip():
            raise ValueError("agent_id must be a non-empty string")

        if self.organization_id is not None:
            if (
                not isinstance(self.organization_id, str)
                or not self.organization_id.strip()
            ):
                raise ValueError(
                    "organization_id must be a non-empty string or None"
                )


_current_context: ContextVar[AuthorityExecutionContext | None] = ContextVar(
    "madhav_authority_execution_context",
    default=None,
)


def get_authority_execution_context() -> AuthorityExecutionContext | None:
    """Return the context associated with the current execution."""
    return _current_context.get()


@contextmanager
def authority_execution_context(
    agent_id: str,
    organization_id: str | None,
) -> Iterator[AuthorityExecutionContext]:
    """Set execution identity temporarily and restore the previous context."""
    context = AuthorityExecutionContext(
        agent_id=agent_id,
        organization_id=organization_id,
    )
    token = _current_context.set(context)

    try:
        yield context
    finally:
        _current_context.reset(token)