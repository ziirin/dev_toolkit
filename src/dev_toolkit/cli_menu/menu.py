from pathlib import Path

from prompt_toolkit.validation import Validator
from prompt_toolkit.widgets import Box, Button, Dialog, Label
from prompt_toolkit.layout import D, FormattedTextControl, HSplit, Layout, ScrollOffsets, VSplit, Window, WindowAlign
from prompt_toolkit.layout.processors import PasswordProcessor
from prompt_toolkit.application import Application, get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import (input_dialog,
                                      clear as _clear,
                                      prompt as _prompt)

from src.dev_toolkit.cli_menu.controls import CustomRadioList
from src.dev_toolkit.cli_menu.validators import FileOrFolderValidator
from src.dev_toolkit.cli_menu.routing import (DevTool, MENU_ROUTING, BASE_PATH)
from src.dev_toolkit.config.app_config import APP_CONFIG, APP_PATHS, decode_PK
from src.dev_toolkit.misc.cli_style import ONE_ATOM_THEME, ONE_ATOM_PALETTE
from src.dev_toolkit.misc.util import get_args_from_path
from src.dev_toolkit.misc.launcher import run_ps_command

# ========================================================================

def _get_title_from_path(menu_path: str) -> str:
    title_array = menu_path.split('/')
    title_array.pop(0)
    if len(title_array) > 0 and title_array[0] == 'devtoolkit':
        title_array[0] = 'DevToolkit'
        
    title_array = [n.capitalize().replace('_', ' ') for n in title_array]
    title = ' → '.join(title_array)
    return title

def _filter_options(options: list[tuple[str, str, bool]]) -> list[tuple[str, str]]:
    fx = (lambda opt: MENU_ROUTING.get(opt[0].split('?')[0], None))
    filtered_opts = list(filter(fx, options))
    
    return filtered_opts

def _print_simple_msg(title:str, text: str) -> str:
    kb = KeyBindings()
    
    @kb.add('right')
    def _(event):
        event.app.exit(result=BASE_PATH)
    
    ok_button = Button(
        text='Ok',
        handler=lambda: get_app().exit(result=BASE_PATH)
    )
    
    dialog = Dialog(
        title=title,
        body=HSplit([
            Label(text=text)
        ]),
        buttons=[ok_button],
        with_background=True
    )
    
    app = Application(
        layout=Layout(dialog),
        key_bindings=kb,
        style=ONE_ATOM_THEME,
        full_screen=True,
        mouse_support=True
    )
    
    return app.run()

def print_radiolist_menu(title: str, text: str,
                         options: list[tuple[str, str, bool]],
                         right_side_info: str | None = None,
                         filter_options: bool = False) -> str:
    result = None
    if filter_options:
        options = _filter_options(options)
    if len(options) > 0:
        radio_list = CustomRadioList(values=options)
        is_root = (title == 'DevToolkit')
        
        scrollable_menu = Window(
            content=radio_list.control,
            height=D(max=min(len(options), 10)),
            scroll_offsets=ScrollOffsets(top=1, bottom=1),
            dont_extend_height=False
        )
        
        dialog_content = [
            Box(scrollable_menu, padding=1),
        ]
        
        if right_side_info:
            dialog_content.append(
                Label(
                    text=right_side_info,
                    style=ONE_ATOM_PALETTE['muted_text'],
                    align=WindowAlign.RIGHT))
        
        dialog = Dialog(
            title=title,
            body=HSplit([
                Label(text=text, dont_extend_height=True),
                VSplit(dialog_content, padding=5)
            ]),
            buttons=[
                Button(text="Ok", handler=lambda: get_app().exit(result=radio_list.current_value)),
                Button(text='Exit' if is_root else 'Back', handler=lambda: get_app().exit(result=None))
            ],
            with_background=True
        )
        
        global_kb = KeyBindings()
        @global_kb.add('c-p')
        def _(event):
            get_app().exit(result=f'{BASE_PATH}/admin')
        
        app = Application(
            layout=Layout(dialog),
            key_bindings=global_kb,
            style=ONE_ATOM_THEME,
            full_screen=True,
            mouse_support=True
            # cursor=None
        )
        
        app.layout.focus(radio_list.control)
        
        return app.run()
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
        text=f'⚠  {args.get("msg", "Unexpected error.")}'
    )
    return (None
            if APP_CONFIG.get('close_after_err', False)
            else result)

@DevTool('')
def _print_main_menu(menu_path: str) -> str | None:
    options = [
        (BASE_PATH + '/tsilang', 'Tsilang tools', 'submenu'),
        (BASE_PATH + '/rad', 'RAD Studio tools', 'submenu'),
        (BASE_PATH + '/git', 'Git', 'submenu'),
        (BASE_PATH + '/inescop', 'Inescop tools', 'submenu'),
        (BASE_PATH + '/task_manager', 'Task manager', 'submenu'),
        (BASE_PATH + '/common_links', 'Common links', 'submenu')
    ]
    
    return print_radiolist_menu(
        _get_title_from_path(menu_path),
        'Choose a tool:',
        options
    )

@DevTool('/tsilang')
def _print_tsilang_menu(menu_path: str) -> str:
    options = [
        (BASE_PATH + '/tsilang/:load', 'Load SILs to DFM', None),
        (BASE_PATH + '/tsilang/:save', 'Save SILs from DFM', None),
        (BASE_PATH + '/tsilang/:clear', 'Clear SILs.', None),
        (BASE_PATH + '/tsilang/:sil2csv', 'Convert SIL to CSV', None),
        (BASE_PATH + '/tsilang/:csv2sil', 'Convert CSV to SIL', None),
    ]
    
    title = _get_title_from_path(menu_path)
    result = print_radiolist_menu(
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
            
        except:
            return f'{BASE_PATH}/err?msg=An error has occurred whilst reading one of the paths.'
    
        return f'{result}?in={input_file}&out={output_file}'
    
    else:
        return result

@DevTool('/rad')
def _print_rad_menu(menu_path: str) -> str:
    options = [
        (BASE_PATH + '/rad/:platform_changer?preset=debug', 'Platform changer: w32 Debug', None),
        (BASE_PATH + '/rad/:platform_changer?preset=release', 'Platform changer: w64 Release', None),
        (BASE_PATH + f'/:run_ps_script?path={APP_PATHS.get("KILL_RAD")}', 'Kill TwineCompile subprocesses', None),
        (BASE_PATH + f'/:run_ps_script?path={APP_PATHS.get("CLEAN_RAD")}', 'Clean temporal files and folders', None)
    ]
    
    title = _get_title_from_path(menu_path)
    return print_radiolist_menu(
        title,
        'Choose an option:',
        options
    )

@DevTool('/git')
def _print_git_menu(menu_path: str) -> str:
    options = [
        (BASE_PATH + '/git/:stash_save', 'Stash changes', None),
        (BASE_PATH + '/git/:stash_bring_back', 'Bring back changes', None),
        (BASE_PATH + '/git/:discard', 'Discard changes', 'warning'),
        (BASE_PATH + '/git/:force_develop', 'Force move to develop', 'warning')
    ]
    
    repo_path = APP_CONFIG.get('global', {}).get('main_src_folder', '')
    cmd = f'git -C "{repo_path}" branch --show-current'
    cur_branch_res, cur_branch = run_ps_command(cmd.split(' '))
    
    result = print_radiolist_menu(
        _get_title_from_path(menu_path),
        'Choose a tool:',
        options,
        f'Current branch: {cur_branch}' if cur_branch_res else ''
    )
    
    return result

@DevTool('/inescop')
def _print_inescop_menu(menu_path: str) -> str:
    password_params = ''
    encoded_pass = APP_CONFIG.get('passwords', {}).get('inescop')
    if encoded_pass:
        password = decode_PK(encoded_pass)
        password_params = f'&auto_type="{password}"&auto_enter=True'
    
    options = [
        (BASE_PATH + f'/:run_exe_detached?path={APP_PATHS.get("SOLYDOC", "")}{password_params}', 'Solydoc', None),
        (BASE_PATH + f'/:run_exe_detached?path={APP_PATHS.get("GESPRO", "")}{password_params}', 'Gespro', None),
        (BASE_PATH + f'/:run_shortcut?path={APP_PATHS.get("CREATE_INSTALLERS", "")}', 'Create installers', None),
        (BASE_PATH + f'/inescop/:backup?src_folder={APP_CONFIG.get("global", {}).get("main_src_folder", "")}', 'Create src folder backup', None),
        (BASE_PATH + '/inescop/:search_icons', 'Search Icons.', None),
        (BASE_PATH + f'/:run_ps_script?path={APP_PATHS.get("RM_INKS_TMP_FILE")}', 'Remove InkScape tmp files', None)
    ]
    
    result = print_radiolist_menu(
        _get_title_from_path(menu_path),
        'Choose a tool:',
        options
    )
    
    return result

@DevTool('/admin')
def _print_admin_menu(menu_path: str) -> str:
    options = [
        (BASE_PATH + '/inescop/:search_icons?update=true', 'Regenerate search icons file', False),
        (BASE_PATH + '/admin/:add_password', 'Add password', 'warning'),
        (BASE_PATH + '/admin/:encode_file', 'Encode file', 'warning')
    ]
    
    result = print_radiolist_menu(
        _get_title_from_path(menu_path),
        'Choose a tool:',
        options
    )
    
    return result

@DevTool('/task_manager')
def _print_task_manager_menu(menu_path: str) -> str:
    options = [
        (BASE_PATH + f'/task_manager/:render_task_md', 'MarkDown view', None),
        (BASE_PATH + f'/task_manager/:add_task', 'Add task', None),
        (BASE_PATH + f'/task_manager/:add_note', 'Add note to task', None),
        (BASE_PATH + f'/task_manager/:change_task_order', 'Change order', 'submenu'),
        (BASE_PATH + f'/task_manager/:task_done', 'Mark task as done', 'submenu'),
        (BASE_PATH + f'/task_manager/:task_remove', 'Remove task', 'warning')
    ]
    
    result = print_radiolist_menu(
        _get_title_from_path(menu_path),
        'Choose an option:',
        options
    )
    
    return result

@DevTool('/common_links')
def _print_common_links_menu(menu_path: str) -> str:
    options = [
        (BASE_PATH + f'/:open_browser?url={APP_PATHS.get("ICAD_WORKSPACE", "")}', 'ICad Workspace', None),
        (BASE_PATH + f'/:open_browser?url={APP_PATHS.get("TICKET_PLATFORM", "")}', 'Ticket platform', None),
        (BASE_PATH + f'/:open_browser?url={APP_PATHS.get("CALCULAHORA", "")}', 'Calculahora®', None),
        (BASE_PATH + f'/:open_browser?url={APP_PATHS.get("CHAT_GPT", "")}', 'AI: ChatGPT', None),
        (BASE_PATH + f'/:open_browser?url={APP_PATHS.get("GEMINI", "")}', 'AI: Gemini', None),
        (BASE_PATH + f'/:open_browser?url={APP_PATHS.get("CLAUDE", "")}', 'AI: Claude', None)
    ]
    
    result = print_radiolist_menu(
        _get_title_from_path(menu_path),
        'Select a link:',
        options
    )
    
    return result

# ========================================================================

def prompt(msg: str, validator: Validator | None = None,
           placeholder: str | None = None,
           default: str | None = None,
           is_password: bool | None = None,
           rprompt: str | None = None,
           bottom_toolbar: str | None = None,
           clear = True) -> str:
    if clear:
        _clear()
    input_processors = []
    if is_password:
        input_processors.append(PasswordProcessor(char='•'))

    return _prompt(f'> {msg}: ',
                   input_processors=input_processors,
                   wrap_lines=True,
                   validator=validator,
                   validate_while_typing=(validator != None),
                   placeholder=placeholder,
                   default=default if default else '',
                   is_password=is_password,
                   rprompt=rprompt,
                   bottom_toolbar=bottom_toolbar,
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
                is_success_path = menu_path.startswith(BASE_PATH + '/success?')
                is_err_path = menu_path.startswith(BASE_PATH + '/err?')
                
                if is_success_path and APP_CONFIG.get('close_after_success', False):
                    default_result = None
                if is_err_path and APP_CONFIG.get('close_after_err', False):
                    default_result = None
                if default_result:
                    _clear()
                    
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
        resolve_path(f'{BASE_PATH}/err?msg=Path "{menu_path}" not found.')
        return None
