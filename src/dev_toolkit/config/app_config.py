import os
import json

# Path to config.json
CONFIG_FILE = './src/config.json'

# This is the default configuration
# This configuration can be changed using config.json
APP_CONFIG = {
    'close_after_success': True,
    'close_after_err': False,
    'allowed_tools': [
        # Entrypoint
        '/devtoolkit',
        
        # devtoolkit > tsilang
        '/devtoolkit/tsilang',
        '/devtoolkit/tsilang/:sil2csv',
        '/devtoolkit/tsilang/:csv2sil',
        
        # devtoolkit > git
        # '/devtoolkit/git',
        
        # devtoolkit > :kill_rad
        # '/devtoolkit/:kill_rad',
        
        # devtoolkit > :icons_web
        # '/devtoolkit/:icons_web',
        
        # devtoolkit > settings
        # '/devtoolkit/settings'
    ]
}

def load_config() -> None:
    global APP_CONFIG
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as config_file:
            APP_CONFIG |= json.load(config_file)