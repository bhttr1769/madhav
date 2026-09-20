from uuid import uuid4


class EvolutionIdGenerator:
    def generate(self) -> str:
        return f"evo-{uuid4().hex}"