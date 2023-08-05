import os
import json
from pathlib import Path


def get_mapping_from_env(var):
    mapping = os.environ.get(var, None)
    if mapping is None:
        return None
    else:
        return {
            key: os.path.expandvars(name) for key, name in json.loads(mapping).items()
        }


# set default paths
DEFAULT_APP_DIR = Path(os.path.expandvars(os.environ.get("FG_APP_DIR", "/app")))
DEFAULT_DATA_ROOT = Path(
    os.path.expandvars(os.environ.get("FG_DATA_ROOT", "/fastgenomics"))
)
INPUT_FILE_MAPPING = get_mapping_from_env("INPUT_FILE_MAPPING")


# summary key for the FGProcess.output
SUMMARY_KEY = "summary"
