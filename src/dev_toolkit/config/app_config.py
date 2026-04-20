import os
import sys
import json
from pathlib import Path

# Path to config.json
if getattr(sys, 'frozen', False):
    # Used from .exe file
    CONFIG_FILE = str(Path(sys.executable).parent / 'config.json')
else:
    # Used from .py file
    CONFIG_FILE = str(Path(sys.argv[0]).parent / 'config.json')

# This is the default configuration
# This configuration can be changed using config.json
APP_CONFIG = {
    'close_after_success': True,
    'close_after_err': False,
    'global': {
        'main_src_folder': 'c:/fuentes/nucleo'
    },
    'modules': {
    },
    'allowed_tools': [
        '/devtoolkit',
        '/devtoolkit/tsilang',
        '/devtoolkit/tsilang/:sil2csv',
        '/devtoolkit/tsilang/:csv2sil',
        '/devtoolkit/tsilang/:clear',
        '/devtoolkit/:kill_rad',
        # '/devtoolkit/:calculahora'
        '/devtoolkit/common_links',
        "/devtoolkit/common_links/:ticket_platform",
        "/devtoolkit/common_links/:ia_gpt",
        "/devtoolkit/common_links/:ia_gemini",
        "/devtoolkit/common_links/:ia_claude"
    ]
}

def load_config() -> None:
    global APP_CONFIG
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as config_file:
            APP_CONFIG |= json.load(config_file)