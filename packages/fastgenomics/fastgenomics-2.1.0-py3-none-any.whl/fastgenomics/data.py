from pathlib import Path
from logging import getLogger
import json

from .defaults import DEFAULT_DATA_ROOT, INPUT_FILE_MAPPING

logger = getLogger(f"fastgenomics.data")

DATA_SUBDIRS = ["data", "config", "output", "summary"]
MANDATORY_SUBDIRS = ["data", "config"]


class FGData(object):
    """This class stores the paths to data structured according to the
fastgenomics specification.  It also loads the input file mappings and
checks if the files exist.

    """

    _subdirs = DATA_SUBDIRS
    _mandatory_files = MANDATORY_SUBDIRS

    def __init__(
        self, data_root=DEFAULT_DATA_ROOT, env_input_file_mapping=INPUT_FILE_MAPPING
    ):
        if isinstance(data_root, str):
            data_root = Path(data_root)
        self.root = data_root
        self.env_input_file_mapping = env_input_file_mapping
        self.check_files()

        self.paths = self.get_paths()
        self.input_file_mapping = self.get_input_file_mapping()
        self.parameters = self.get_parameters()

    def get_input_file_mapping(self):
        mapping_file = self.paths["config"] / "input_file_mapping.json"

        if self.env_input_file_mapping is not None and mapping_file.exists():
            raise RuntimeError(
                f'Environmental variable INPUT_FILE_MAPPING was defined and a mapping file "{mapping_file}" was found.  Please use just one of the abouve to define the input file mapping.'
            )
        elif self.env_input_file_mapping is not None:
            logger.debug(
                'Loading the file mapping from an environmental variable "INPUT_FILE_MAPPING".'
            )
            mapping = self.env_input_file_mapping
        elif mapping_file.exists():
            logger.debug(
                f'Loading the input file mapping from a file "{mapping_file}".  The current version of FASTGenomics runtime uses an environmental variable INPUT_FILE_MAPPING to pass the information on file mapping and the file "input_file_mapping.json" should only be used for testing.'
            )
            mapping = json.loads(mapping_file.read_text())
        else:
            raise RuntimeError(
                f'Environmental variable INPUT_FILE_MAPPING was undefined and a mapping file was not found under "{mapping_file}".  Please use one or the other to define the file mapping.'
            )

        logger.debug(f'File mapping is: "{mapping}"')
        return mapping

    def get_paths(self):
        return {dir: self.root / dir for dir in self._subdirs}

    def get_parameters(self):
        params_file = self.paths["config"] / "parameters.json"
        if params_file.exists():
            return json.loads(params_file.read_text())
        else:
            return {}

    def check_files(self):
        if not self.root.exists():
            raise FileNotFoundError(
                f"Could not find the data directory under {self.root}"
            )

        not_found = []
        for f in self._mandatory_files:
            absolute_path = self.root / f
            if not absolute_path.exists():
                not_found.append(f)

        if not_found:
            msg = [
                f'Could not find the following files or directories in "{self.root}":'
            ]
            msg += [f"- {file}" for file in not_found]
            raise FileNotFoundError("\n".join(msg))
