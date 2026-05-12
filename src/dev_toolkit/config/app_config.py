import os
import sys
import json
from pathlib import Path

if getattr(sys, 'frozen', False):
    # Used from .exe file
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    # Used from .py file
    BASE_DIR = Path(sys.argv[0]).resolve().parent
   
# Path to config.json
CONFIG_FILE = str(BASE_DIR / 'assets' / 'config.json')

# This is the default configuration
# This configuration can be changed using config.json
APP_CONFIG = {
    'close_after_success': False,
    'close_after_err': False,
    'global': {
        'main_src_folder': 'c:/fuentes/nucleo',
        'backup_folder': 'd:/backup',
        'icons_folder': '//backup-fa/FA/Iconos'
    }
}

APP_PATHS = {
    'KILL_RAD': str(BASE_DIR / 'assets' / 'scripts' / 'kill_rad.ps1'),
    'CLEAN_RAD': str(BASE_DIR / 'assets' / 'scripts' / 'clean_rad.ps1'),
    'LOAD_SILS': str(BASE_DIR / 'assets' / 'scripts' / 'load_sils.bat'),
    'SAVE_SILS': str(BASE_DIR / 'assets' / 'scripts' / 'save_sils.exe'),
    'SOLYDOC': str(Path('C:/BDINESCOP/Programas/SOLYDOC/solydoc.exe')),
    'GESPRO': str(Path('C:/BDINESCOP/Programas/GESPRO/GestionProyectos.exe')),
    'CREATE_INSTALLERS': str(BASE_DIR / 'assets' / 'scripts' / 'create_installers.lnk'),
    'TICKET_PLATFORM': 'https://tickets.inescop.es/scp/index.php',
    'CALCULAHORA': 'https://tickets.inescop.es/horas.html',
    'CHAT_GPT': 'https://chatgpt.com/?temporary-chat=true',
    'GEMINI': 'https://gemini.google.com/app',
    'CLAUDE': 'https://claude.ai/new'
}

def load_config() -> None:
    global APP_CONFIG
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as config_file:
            APP_CONFIG |= json.load(config_file)