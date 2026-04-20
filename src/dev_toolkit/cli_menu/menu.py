from pathlib import Path

from prompt_toolkit.shortcuts import (message_dialog,
                                      radiolist_dialog,
                                      button_dialog,
                                      input_dialog,
                                      clear as _clear,
                                      prompt as _prompt)
from prompt_toolkit.validation import Validator

from ..cli_menu.validators import FileOrFolderValidator
from ..config.app_config import APP_CONFIG
from .routing import (DevTool, MENU_ROUTING, BASE_PATH)
from ..misc.cli_style import ONE_ATOM_THEME
from ..misc.util import get_args_from_path

# ========================================================================

def _get_title_from_path(menu_path: str) -> str:
    title_array = menu_path.split('/')
    title_array.pop(0)
    if len(title_array) > 0 and title_array[0] == 'devtoolkit':
        title_array[0] = 'DevToolkit'
    title = ' → '.join(title_array)
    return title

def _filter_options(options: list[tuple[str, str]]) -> list[tuple[str, str]]:
    allowed_tools = APP_CONFIG.get('allowed_tools', None)
    if allowed_tools:
        fx = (lambda opt: opt[0] in allowed_tools and MENU_ROUTING.get(opt[0], None))
        filtered_opts = list(filter(fx, options))
    else:
        filtered_opts = options.copy()
    return filtered_opts

def _print_simple_msg(title:str, text: str) -> str:
    result = button_dialog(
        title=title,
        text=text,
        buttons=[('Ok', BASE_PATH)],
        style=ONE_ATOM_THEME
    ).run()
    
    return result

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
    else:
        result = f'{BASE_PATH}/err?msg=No hay opciones disponibles en este menú.'

    return result

def _print_text_input(title: str, text: str,
                 default: str = '',
                 validator: Validator | None = None) -> str:
    return input_dialog(
        title=title,
        text=text,
        default=default,
        validator=validator,
        style=ONE_ATOM_THEME).run()

# ========================================================================

@DevTool('/success')
def _print_success_menu(menu_path: str) -> None:
    args = get_args_from_path(menu_path)
    result = _print_simple_msg(
        title='DevToolkit → Success',
        text=args.get('msg', 'Success.')
    )
    return result

@DevTool('/err')
def _print_err_menu(menu_path: str) -> str | None:
    args = get_args_from_path(menu_path)
    result = _print_simple_msg(
        title='DevToolkit → Error',
        text=args.get('msg', 'Unexpected error.')
    )
    return (None
            if APP_CONFIG.get('close_after_err', False)
            else result)

@DevTool('')
def _print_main_menu(menu_path: str) -> str | None:
    options = [
        (BASE_PATH + '/tsilang', 'Tsilang tools...'),
        (BASE_PATH + '/:kill_rad', 'Kill RAD Studio subprocesses and clean projects.'),
        (BASE_PATH + '/:calculahora', 'Launch Calculahora®.'),
        (BASE_PATH + '/common_links', 'Common links...')
    ]
    
    return _print_radiolist_menu(
        _get_title_from_path(menu_path),
        'Choose a tool:',
        options
    )

@DevTool('/tsilang')    
def _print_tsilang_menu(menu_path: str) -> str:
    options = [
        (BASE_PATH + '/tsilang/:sil2csv', 'Convert SIL to CSV.'),
        (BASE_PATH + '/tsilang/:csv2sil', 'Convert CSV to SIL.'),
        (BASE_PATH + '/tsilang/:clear', 'Clear DFM content.'),
    ]
    
    title = _get_title_from_path(menu_path)
    result = _print_radiolist_menu(
        title,
        'Choose an option:',
        options
    )
    
    if result in ['/devtoolkit/tsilang/:sil2csv', '/devtoolkit/tsilang/:csv2sil']:
        try:
            input_file = Path(
                prompt(
                    msg='Input path',
                    validator=FileOrFolderValidator(),
                    default=str(Path(APP_CONFIG.get('global', {}).get('main_src_folder', '')))
                )
            )
            
            output_file = Path(
                prompt(
                    msg='Output path',
                    default=str(Path.home() / 'Desktop'),
                    clear=False
                )
            )
            
            # input_file = Path(
            #     _print_text_input(
            #         title=title,
            #         text='Input file',
            #         default=str(Path(APP_CONFIG.get('global', {}).get('main_src_folder', ''))),
            #         validator=ValidFileValidator()
            #     )
            # )
            # if not input_file.exists():
            #     return f'{BASE_PATH}/err?msg=File not found: "{input_file}".'
            
            # output_file = Path(
            #     _print_text_input(
            #         title=title,
            #         text='Output file',
            #         default=str(Path.home() / 'Desktop')
            #     )
            # )
        except Exception as e:
            return f'{BASE_PATH}/err?msg=An error has occurred whilst reading one of the paths.'
    
        return f'{result}?in={input_file}&out={output_file}'
    
    else:
        return result

@DevTool('/common_links')
def _print_common_links_menu(menu_path: str) -> str:
    options = [
        (BASE_PATH + '/common_links/:ticket_platform', 'Ticket platform.'),
        (BASE_PATH + '/common_links/:ia_gpt', 'IA: ChatGPT.'),
        (BASE_PATH + '/common_links/:ia_gemini', 'IA: Gemini.'),
        (BASE_PATH + '/common_links/:ia_claude', 'IA: Claude.')
    ]
    
    result = _print_radiolist_menu(
        _get_title_from_path(menu_path),
        'Select a link:',
        options
    )
    
    return result

# ========================================================================

def prompt(msg: str, validator: Validator | None = None,
           placeholder: str | None = None,
           default: str | None = None,
           clear = True) -> str:
    if clear:
        _clear()
    return _prompt(f'> {msg}: ',
                  validator=validator,
                  validate_while_typing=(validator != None),
                  placeholder=placeholder,
                  default=default if default else '',
                  style=ONE_ATOM_THEME)

def resolve_path(menu_path: str = BASE_PATH) -> str | None:
    if menu_path.endswith('/'):
        menu_path = menu_path[:-1]

    path_to_check = menu_path.split('?')[0]
    if path_to_check in MENU_ROUTING.keys():
        result = MENU_ROUTING[path_to_check](menu_path)
        
        # If result!=None we need to resolve the new path
        if result:
            # If result it's equals to BASE_PATH, we need to check
            # close_after_success and close_after_err values to know what to do.
            # This avoids infinite pile of calls
            if result == BASE_PATH:
                default_result = BASE_PATH
                is_success_path = menu_path.startswith(BASE_PATH + '/success')
                is_err_path = menu_path.startswith(BASE_PATH + '/err')
                
                if is_success_path and APP_CONFIG.get('close_after_success', False):
                    default_result = None
                if is_err_path and APP_CONFIG.get('close_after_err', False):
                    default_result = None
                    
                return default_result
            
            # If result it's not base path, we resolve the path
            else:
                return resolve_path(result)
            
        # If result==None means 'Back' or 'Exit' button has been pressed.
        # We need to find out whichone
        else:
            splitted_path = (path_to_check.split('/'))
            back_path = '/'.join(splitted_path[:-1])
            return None if len(splitted_path[:-1]) == 1 else back_path

    else:
        message_dialog('Error', f'Path "{menu_path}" not found.',
                       style=ONE_ATOM_THEME).run()
        return None
