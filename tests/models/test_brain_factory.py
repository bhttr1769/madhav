from brain.factories.brain_factory import BrainFactory
from brain.manager import BrainManager


def test_brain_factory_creates_manager():
    manager = BrainFactory.create()
    assert isinstance(manager, BrainManager)