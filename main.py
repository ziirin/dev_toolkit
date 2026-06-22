import argparse

from prompt_toolkit.shortcuts import clear

from src.dev_toolkit.cli_menu import menu
from src.dev_toolkit.config.app_config import load_config

# Import to load MENU_ROUTING
from src.dev_toolkit.modules import *

# ========================================================================

if __name__ == '__main__':
    program_description = """
    DevToolkit ~ J.Salas (2026)
    Command-line interface program that consolidates several useful developer utilities.
    """
    parser = argparse.ArgumentParser(description=program_description)
    
    parser.add_argument('--path',
                        dest='init_path',
                        default=menu.BASE_PATH,
                        help='Path used as init path when the program is started.')
    
    args = parser.parse_args()
    load_config()
    
    # --
    # Main loop   
    next_path = args.init_path
    while next_path:
        next_path = menu.resolve_path(next_path)

    # --
    # Clear before close
    clear()