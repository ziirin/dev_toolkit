import argparse
from .dev_toolkit.cli_menu import menu

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
                        default='/devtoolkit')
    
    args = parser.parse_args()
    
    # --
    
    # Main loop
    result = 'N/A'
    while result:
        result = menu.print_menu(args.init_path)   