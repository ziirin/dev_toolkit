import os
import json
from .app_config import (APP_CONFIG, _IS_CONFIG_INITIALIZED)

CONFIG_FILE = './src/config.json'

if not _IS_CONFIG_INITIALIZED:
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as config_file:
            tmp_config = json.load(config_file)
            APP_CONFIG = (APP_CONFIG | tmp_config)
    _IS_CONFIG_INITIALIZED = True

__all__ = [
    'APP_CONFIG'
]