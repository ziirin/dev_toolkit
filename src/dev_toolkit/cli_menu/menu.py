from prompt_toolkit.shortcuts import (message_dialog, radiolist_dialog)
from ..misc.cli_style import ONE_ATOM_THEME
from ..config.app_config import APP_CONFIG
from .routing import (DevTool, MENU_ROUTING)

# ========================================================================

def _filter_options(options: list[tuple[str, str]]) -> list[tuple[str, str]]:
    allowed_tools = APP_CONFIG.get('allowed_tools', None)
    if allowed_tools:
        fx = (lambda opt: opt[0] in allowed_tools and MENU_ROUTING.get(opt[0], None))
        filtered_opts = list(filter(fx, options))
    else:
        filtered_opts = options.copy()
    return filtered_opts

def _print_radiolist_menu(title: str, text: str,
                          options: list[tuple[str, str]]) -> str:
    result = None
    options = _filter_options(options)
    if len(options) > 0:
        result = radiolist_dialog(
            title=title,
            text=text,
            cancel_text='Exit' if title == 'DevToolkit' else 'Back',
            values=options,
            style=ONE_ATOM_THEME
        ).run()
    
    return result

# ========================================================================

@DevTool('/devtoolkit')
def _print_main_menu() -> str | None:
    options = [
        ('/devtoolkit/tsilang', 'Tsilang options...'),
        ('/devtoolkit/git', 'Git options...'),
        ('/devtoolkit~kill_rad', 'Kill RAD Studio subprocesses and clean projects.'),
        ('/devtoolkit~icons_web', 'Generate a icons web to search ICad icons.'),
        ('/devtoolkit/settings', 'Settings...')
    ]
    
    return _print_radiolist_menu(
        'DevToolkit',
        'Choose a tool:',
        options
    )

@DevTool('/devtoolkit/tsilang')    
def _print_tsilang_menu() -> str:
    options = [
        ('/devtoolkit/tsilang~sil2csv', 'Convert SIL to CSV.'),
        ('/devtoolkit/tsilang~csv2sil', 'Convert CSV to SIL.')
    ]
    
    return _print_radiolist_menu(
        'DevToolkit → Tsilang',
        'Choose a tool:',
        options
    )

# ========================================================================

def print_menu(menu_path: str = '/devtoolkit') -> str | None:
    if menu_path.endswith('/'):
        menu_path = menu_path[:-1]

    if menu_path in MENU_ROUTING.keys():
        result = MENU_ROUTING[menu_path]()
        menu_path_splitted = menu_path.split('/')
        if not result and len(menu_path_splitted) > 1:
            result = '/'.join(menu_path_splitted[:-1])
        if result and '~' not in result:
            print_menu(result)

    else:
        message_dialog('Error', f'Path "{menu_path}" not found.',
                       style=ONE_ATOM_THEME).run()
