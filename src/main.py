import argparse
from .dev_toolkit.cli_menu import menu
from .dev_toolkit.config.app_config import load_config

# Import to load MENU_ROUTING
from .dev_toolkit.modules import *

# ========================================================================

if __name__ == '__main__':
    program_description = """
    DevToolkit ~ J.Salas (2026)
    Command-line interface program that consolidates several useful developer utilities.
    """
    parser = argparse.ArgumentParser(description=program_description)
    
    parser.add_argument('--initial-path',
                        dest='init_path',
                        default=menu.BASE_PATH)
    
    args = parser.parse_args()
    load_config()
    
    # --
    # Main loop
    next_path = args.init_path if args.init_path else menu.BASE_PATH
    while next_path:
        next_path = menu.resolve_path(next_path)