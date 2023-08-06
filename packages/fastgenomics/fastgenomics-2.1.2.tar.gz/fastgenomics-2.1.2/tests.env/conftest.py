import os
import pytest


@pytest.fixture
def env_mapping():
    print(os.environ["INPUT_FILE_MAPPING"])
