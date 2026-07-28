import pytest

from brain.exceptions.errors import UnsupportedFileTypeError
from brain.manager import BrainManager


def test_unsupported_file_type():

    manager = BrainManager()

    with pytest.raises(UnsupportedFileTypeError):
        manager.read("sample.xyz")