from brain.agents.agent_runtime import AgentRuntime


class AgentRuntimeRegistry:
    def __init__(self):
        self._runtimes: dict[str, AgentRuntime] = {}

    def register(self, runtime: AgentRuntime) -> None:
        if not isinstance(runtime, AgentRuntime):
            raise TypeError(
                "runtime must be an AgentRuntime"
            )

        runtime_id = runtime.runtime_id

        if runtime_id in self._runtimes:
            raise ValueError(
                f"runtime already registered: {runtime_id}"
            )

        self._runtimes[runtime_id] = runtime

    def get(self, runtime_id: str) -> AgentRuntime:
        if not isinstance(runtime_id, str):
            raise TypeError(
                "runtime_id must be a string"
            )

        if not runtime_id.strip():
            raise ValueError(
                "runtime_id must not be empty"
            )

        return self._runtimes[runtime_id]

    def has(self, runtime_id: str) -> bool:
        if not isinstance(runtime_id, str):
            raise TypeError(
                "runtime_id must be a string"
            )

        if not runtime_id.strip():
            raise ValueError(
                "runtime_id must not be empty"
            )

        return runtime_id in self._runtimes

    def all(self) -> tuple[AgentRuntime, ...]:
        return tuple(self._runtimes.values())

    def unregister(self, runtime_id: str) -> None:
        if not isinstance(runtime_id, str):
            raise TypeError(
                "runtime_id must be a string"
            )

        if not runtime_id.strip():
            raise ValueError(
                "runtime_id must not be empty"
            )

        del self._runtimes[runtime_id]