from typing import *
import os
from pathlib import Path
from fifteenrock.lib import util


def default_config_path(credentials_file='fifteenrock.json'):
    return Path(os.getcwd()) / credentials_file


def determine_credentials(path: Path = None) -> Dict:
    _path = path or default_config_path()
    return util.read_json(_path)['default']
