import os
import datetime
import subprocess
from uuid import uuid4
from pathlib import Path

from src.dev_toolkit.cli_menu.validators import BoolValidator, FileValidator, NoEmptyValidator, NotFileOrFolderValidator, NumberValidator, TaskNameValidator
from src.dev_toolkit.cli_menu.routing import DevTool
from src.dev_toolkit.cli_menu.menu import BASE_PATH, print_radiolist_menu, prompt
from src.dev_toolkit.modules.tasks.tasks import render_task_md
from src.dev_toolkit.modules.icons.icons import render_html_icon_list
from src.dev_toolkit.modules.backup.backup import create_backup
from src.dev_toolkit.modules.platform_changer import platform_changer
from src.dev_toolkit.misc import get_args_from_path
from src.dev_toolkit.config.app_config import APP_CONFIG, APP_PATHS, encode_PK, save_config
from src.dev_toolkit.modules.tsilang.clear_translations import remove_translation_data
from src.dev_toolkit.misc.launcher import open_url, run_bat_script, run_exe_detached, run_exe_script, run_ps_command, run_ps_script, run_shortcut
from src.dev_toolkit.modules.encrypt.encode import encode_file_to_images
from src.dev_toolkit.modules.tsilang.silFixer import (read_sil,
                                                      write_sil,
                                                      read_csv,
                                                      write_csv,
                                                      get_lang_names)

# ========================================================================

@DevTool('/tsilang/:sil2csv')
def _handle_sil2csv(menu_path: str) -> str:
    args = get_args_from_path(menu_path)
    result = BASE_PATH
    
    input_path = args.get('in', '')
    output_path = args.get('out', '')
    
    # Converting file
    if Path(input_path).is_file():
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        sil_data = read_sil(input_path, get_lang_names())[0]
        write_csv(output_path, sil_data)
        result += f'/success?msg=File succesfully converted ({output_path}).'
        
    # Converting files from folder
    elif Path(input_path).is_dir(): # and Path(output_path).is_dir():
        files = list(Path(input_path).rglob('*.sil'))
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        for f in files:
            sil_data = read_sil(f, get_lang_names())[0]
            write_csv(Path(output_path) / f'{f.stem}.csv', sil_data)
        result += f'/success?msg=Files succesfully converted ({output_path}).'
    
    # Some path doesnt exist
    else:
        if not Path(input_path).exists():
            result += f'/err?msg=Following file or directory doesnt exists: {input_path}.'
        elif not Path(output_path).exists():
            result += f'/err?msg=Following file or directory doesnt exists: {output_path}.'
        else:
            result += f'/err?msg=Error at input or output path.'
        
    return result

@DevTool('/tsilang/:csv2sil')
def _handle_csv2sil(menu_path: str) -> str:
    args = get_args_from_path(menu_path)
    result = BASE_PATH
    
    input_path = args.get('in', '')
    output_path = args.get('out', '')
    
    # Converting file
    if Path(input_path).is_file():
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            csv_data = read_csv(input_path)[0]
            write_sil(output_path, csv_data)
            result += f'/success?msg=File succesfully converted ({output_path}).'
        except Exception as e:
            result += f'/err?msg={e}'
            
    # Converting files from folder
    elif Path(input_path).is_dir(): # and Path(output_path).is_dir():
        files = list(Path(input_path).rglob('*.csv'))
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        for f in files:
            csv_data = read_csv(f)[0]
            write_sil(Path(output_path) / f'{f.stem}.sil', csv_data)
        result += f'/success?msg=Files succesfully converted ({output_path}).'
        
    # Some path doesnt exist
    else:
        if not Path(input_path).exists():
            result += f'/err?msg=Following file or directory doesnt exists: {input_path}.'
        elif not Path(output_path).exists():
            result += f'/err?msg=Following file or directory doesnt exists: {output_path}.'
        else:
            result += f'/err?msg=Error at input or output path.'

    return result

@DevTool('/tsilang/:load')
def _handle_load_sil(menu_path: str) -> str:
    result = BASE_PATH
    if run_bat_script(APP_PATHS.get('LOAD_SILS')):
        result += f'/success?msg=Translations loaded.'
    else:
        result += f'/err?msg=An error occurred.'
        
    return result

@DevTool('/tsilang/:save')
def _handle_save_sil(menu_path: str) -> str:
    projects = [
        str(Path('c:/Fuentes/Nucleo/ShoeData')),
        str(Path('c:/Fuentes/Nucleo/Nucleo')),
        str(Path('c:/Fuentes/Nucleo/3DPlus')),
        str(Path('c:/Fuentes/Nucleo/Forma3D')),
        str(Path('c:/Fuentes/Nucleo/Foot3D')),
        str(Path('c:/Fuentes/Nucleo/ICadNest'))
    ]
    
    success = True
    for project in projects:
        success &= run_exe_script(APP_PATHS.get('SAVE_SILS'), [project])
        
    result = BASE_PATH
    if success:
        result += '/success?msg=Translations saved.'
    else:
        result += f'/err?msg=Something went wrong when saving at least one project.'
        
    return result

@DevTool('/tsilang/:clear')
def _handle_clear(menu_path: str) -> str:
    args = get_args_from_path(menu_path)
    result = BASE_PATH
    
    path = args.get('path')
    if path == None:
        path = APP_CONFIG.get('global', {}).get('main_src_folder', '')
    
    if os.path.isdir(path):
        try:
            remove_translation_data(path)
            result += '/success?msg=Translations successfully deleted.'
        except Exception as e:
            result += f'/err?{e}'
    else:
        result += f'/err?msg=Following directory doesnt exists: {path}.'
        
    return result

# ========================================================================

@DevTool('/rad/:platform_changer')
def _handle_platform_changer(menu_path: str) -> str:
    args = get_args_from_path(menu_path)
    preset = args.get('preset', 'debug')
    
    values = {}
    cbproj_files = Path(APP_CONFIG.get('global', {}).get('main_src_folder', '')).rglob('*.cbproj')
    cbproj_folders = {str(f.parent).lower() for f in cbproj_files}
    if preset == 'debug':
        debug_projects = [
            str(Path('c:/fuentes/nucleo/shoedata')),
            
            str(Path('c:/fuentes/nucleo/nucleo/app/geometry')),
            
            str(Path('c:/fuentes/nucleo/nucleo/app/pads')),
            str(Path('c:/fuentes/nucleo/3dplus/app/pads')),
            str(Path('c:/fuentes/nucleo/forma3d/app/pads')),
            str(Path('c:/fuentes/nucleo/foot3d/app/pads')),
            str(Path('c:/fuentes/nucleo/icadnest/app/pads')),
            
            str(Path('c:/fuentes/nucleo/nucleo/app/application')),
            str(Path('c:/fuentes/nucleo/3dplus/app/application')),
            str(Path('c:/fuentes/nucleo/forma3d/app/application')),
            str(Path('c:/fuentes/nucleo/foot3d/app/application')),
            str(Path('c:/fuentes/nucleo/icadnest/app/application')),
            
            str(Path('c:/fuentes/nucleo/3dplus/app')),
            str(Path('c:/fuentes/nucleo/forma3d/app')),
            str(Path('c:/fuentes/nucleo/foot3d/app')),
            str(Path('c:/fuentes/nucleo/icadnest/app')),
        ]
        
        values = dict.fromkeys(cbproj_folders, ['w32', 'Release'])
        for value in values:
            if value.lower() in debug_projects:
                values[value] = ['w32', 'Debug']
        
    elif preset == 'release':
        values = dict.fromkeys(cbproj_folders, ['w64', 'Release'])
    
    if len(values) > 0:
        print(f'Applying "{preset}" preset...')
        platform_changer(values, True)
        result =  f'{BASE_PATH}/success?msg=Platform succesfully changed.'
    else:
        result =  f'{BASE_PATH}/err?msg=No project folder found.'
        
    return result

# ========================================================================

@DevTool('/git/:stash_bring_back')
def _handle_stash_bring_back(menu_path: str) -> str:
    repo_path = APP_CONFIG.get('global', {}).get('main_src_folder', '')
    result = subprocess.run(
        ['git', '-C', repo_path, 'stash', 'list'],
        capture_output=True,
        text=True,
        check=True
    )
    
    strip_result = result.stdout.strip()
    stashes = strip_result.split('\n') if strip_result else []
    stash_options = []
    for (i, stash) in enumerate(stashes):
        stash_options.append((
            'stash@{' + str(i) + '}',
            stash[stash.find('}') + 3:]
        ))
    
    stash_selected = print_radiolist_menu(
        'Stash pop',
        'Select the stash to pop',
        stash_options
    )
    
    run_ps_command([
        'git',
        '-C', f'"{repo_path}"',
        'stash',
        'pop', f'"{stash_selected}"'
    ])
    
    return f'{BASE_PATH}/success?msg=Stash popped successfully.'

@DevTool('/git/:stash_save')
def _handle_stash_save(menu_path: str) -> str:
    repo_path = APP_CONFIG.get('global', {}).get('main_src_folder', '')
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    run_ps_command([
        'git',
        '-C', f'"{repo_path}"',
        'stash',
        'save', f'"DevToolkit stash ({timestamp})"',
        '-u'
    ])
        
    return f'{BASE_PATH}/success?msg=Stash created successfully.'

@DevTool('/git/:discard')
def _handle_discard(menu_path: str) -> str:
    confirmRes = prompt('Do you want to discard ALL changes', validator=BoolValidator(), placeholder='(y/n)')
    
    if confirmRes in BoolValidator.TRUE_VALUES:
        repo_path = APP_CONFIG.get('global', {}).get('main_src_folder', '')
        
        cmd = f'git -C "{repo_path}" restore .'
        run_ps_command(cmd.split(' '))
        
        cmd = f'git -C "{repo_path}" clean -fd'
        run_ps_command(cmd.split(' '))
        
        return f'{BASE_PATH}/success?msg=Changes discarted successfully.'
    
    return BASE_PATH    

# ========================================================================

@DevTool('/inescop/:search_icons')
def _handle_search_icons(menu_path: str) -> str:
    args = get_args_from_path(menu_path)
    update = args.get('update', 'false').lower()
    
    icons_path = APP_CONFIG.get('global', {}).get('icons_folder', '')
    dest_path = '//backup-fa/FA/Iconos/_icon_list.html'
    
    if update == 'true':
        render_html_icon_list(dest_path, icons_path)
        
    return f'{BASE_PATH}/:open_browser?url=file:{dest_path}'

@DevTool('/inescop/:backup')
def _handle_backup(menu_path: str) -> str:
    args = get_args_from_path(menu_path)
    src_folder = args.get('src_folder', APP_CONFIG.get('global', {}).get('main_src_folder', ''))
    rar_file = args.get('rar_file')
    
    backup_folder = APP_CONFIG.get('global', {}).get('backup_folder')
    if not rar_file:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        default_path = str(Path(backup_folder) / f'backup_{timestamp}.rar')
        rar_file = str(Path(prompt('Backup RAR file name', validator=NotFileOrFolderValidator(), default=default_path)))

    result = BASE_PATH
    if create_backup(src_folder, rar_file):
        result += f'/success?msg=Backup done.'
    else:
        result += f'/err?msg=Something went wrong.'
    
    return result

# ========================================================================

@DevTool('/task_manager/:render_task_md')
def _handle_render_task_md(menu_path: str) -> str:
    if not APP_CONFIG.get('tasks'):
        APP_CONFIG['tasks'] = []
    
    filename = Path(f'{APP_PATHS.get("TASKS_MD_FILE", "tmp.md")}').absolute()
    md_content = render_task_md(APP_CONFIG.get('tasks', []))
    with open(filename, 'w', encoding='utf-8') as md_file:
        md_file.write(md_content)
    
    open_url(f'file://{filename}')
    # if filename.exists():
    #     filename.unlink()
        
    return BASE_PATH

@DevTool('/task_manager/:add_task')
def _handle_add_task(menu_path: str) -> str:
    name = prompt('Name', validator=TaskNameValidator())
    ticket = prompt('Ticket #', validator=NumberValidator() ,clear=False)
    description = prompt('Description', clear=False)
    
    if not APP_CONFIG.get('tasks'):
        APP_CONFIG['tasks'] = []
    
    APP_CONFIG['tasks'].append({
        'name': name,
        'ticket': ticket,
        'description': description,
        'notes': [],
        'addition_date': datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
        'done': ''
    })
    save_config()
    
    return f'{BASE_PATH}/success?msg=Task "{name}" added.'

@DevTool('/task_manager/:add_note')
def _handle_add_note(menu_path: str) -> str:
    if not APP_CONFIG.get('tasks'):
        APP_CONFIG['tasks'] = []
        
    options = [(n, task['name']) for n, task in enumerate(APP_CONFIG['tasks']) if not task['done']]
    if len(options) == 0:
        return f'{BASE_PATH}/err?msg=There are no task to do.'
    
    selected_task = print_radiolist_menu(
        title='Add task update',
        text='Select task you want to add a note:',
        options=options,
    )
    update_text = prompt('Note', validator=NoEmptyValidator())
    
    notes = APP_CONFIG['tasks'][selected_task].get('notes', [])
    notes.append(f'[{datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}] {update_text}')
    save_config()
    
    task_name = APP_CONFIG['tasks'][selected_task]['name']
    return f'{BASE_PATH}/success?msg=Note added to "{task_name}".'

@DevTool('/task_manager/:change_task_order')
def _handle_change_task_order(menu_path: str) -> str:
    if not APP_CONFIG.get('tasks'):
        APP_CONFIG['tasks'] = []
    
    pending_tasks = [task for task in APP_CONFIG['tasks'] if not task['done']]
    options = [(n, f'{n + 1}. {task["name"]}') for n, task in enumerate(pending_tasks)]
    if len(options) <= 1:
        return f'{BASE_PATH}/err?msg=There are not enougth task.'
    
    index_A = print_radiolist_menu(
        title='Change task order',
        text='Select task you want to move:',
        options=options,
    )
    
    if not index_A:
        return BASE_PATH
    
    n = 0
    options = []
    selected_task = APP_CONFIG['tasks'][index_A]
    for task in pending_tasks:
        if task['name'] != selected_task['name']:
            options.append((n, f'{n + 1}. {task["name"]}'))
            n += 1
    options.append((n, f'{n + 1}. ...'))
    
    index_B = print_radiolist_menu(
        title='Change task order',
        text='Select task new position:',
        options=options,
    )
    
    if not index_B:
        return BASE_PATH
    
    APP_CONFIG['tasks'].pop(index_A)
    APP_CONFIG['tasks'].insert(index_B, selected_task)
    
    save_config()
    task_name = selected_task['name']
    return f'{BASE_PATH}/success?msg=Task "{task_name}" moved to position {index_B + 1}.'

@DevTool('/task_manager/:task_done')
def _handle_task_done(menu_path: str) -> str:
    if not APP_CONFIG.get('tasks'):
        APP_CONFIG['tasks'] = []
        
    options = [(n, task['name']) for n, task in enumerate(APP_CONFIG['tasks']) if not task['done']]
    if len(options) == 0:
        return f'{BASE_PATH}/err?msg=There are no task to do.'
    
    selected_task = print_radiolist_menu(
        title='Mark task as done',
        text='Select task you want to finish:',
        options=options,
    )
    
    APP_CONFIG['tasks'][selected_task]['done'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    save_config()
    
    return f'{BASE_PATH}/success?msg=Task succesfully closed.'

@DevTool('/task_manager/:task_remove')
def _handle_task_remove(menu_path: str) -> str:
    if not APP_CONFIG.get('tasks'):
        APP_CONFIG['tasks'] = []
        
    options = [(n, task['name']) for n, task in enumerate(APP_CONFIG['tasks']) if not task['done']]
    if len(options) == 0:
        return f'{BASE_PATH}/err?msg=There are no task to do.'
    
    selected_task = print_radiolist_menu(
        title='Remove task',
        text='Select task you want to remove:',
        options=options,
    )
    
    APP_CONFIG['tasks'].pop(selected_task)
    save_config()
    
    return f'{BASE_PATH}/success?msg=Task succesfully removed.'

# ========================================================================

@DevTool('/admin/:add_password')
def _handle_add_password(menu_path: str) -> str:
    name = prompt('Name')
    password = prompt('Password', clear=False, is_password=True)
    encrypted_pass = encode_PK(password)
    
    if not APP_CONFIG.get('passwords'):
        APP_CONFIG['passwords'] = {}
    
    APP_CONFIG['passwords'][name] = encrypted_pass
    save_config()
    
    return f'{BASE_PATH}/success?msg=Password "{name}" added.'

@DevTool('/admin/:encode_file')
def _handle_encode(menu_path: str) -> str:
    args = get_args_from_path(menu_path)
    src_file = Path(args.get('src_file', ''))
    dst_file = Path(args.get('dst_file', src_file.parent / 'img'))
    
    if not src_file.is_file():
        src_file = prompt('File to encript', FileValidator())
    
    try:
        encode_file_to_images(src_file, dst_file)
    except:
        return f'{BASE_PATH}/err?msg=Something went wrong.'
    
    return f'{BASE_PATH}/success?msg=File encoded.'

# ========================================================================

@DevTool('/:open_browser')
def _handle_open_browser(menu_path: str) -> str:
    args = get_args_from_path(menu_path)
    url = args.get('url')
    
    if open_url(url):
        result = BASE_PATH
    else:
        result = f'{BASE_PATH}/err?msg=Cannout launch "{url}".'
    
    return result

@DevTool('/:run_ps_script')
def _handle_run_ps_script(menu_path: str) -> str:
    args = get_args_from_path(menu_path)
    path = args.get('path', '')
    
    if run_ps_script(path):
        result = BASE_PATH
    else:
        result = f'{BASE_PATH}/err?msg=Cannout launch "{path}".'
    
    return result

@DevTool('/:run_exe_detached')
def _handle_run_exe_detached(menu_path: str) -> str:
    args = get_args_from_path(menu_path)
    path = args.get('path')
    auto_type = args.get('auto_type')
    auto_enter = args.get('auto_enter') == 'True'
    
    if run_exe_detached(path):
        result = BASE_PATH
        if auto_type:
            import pyautogui
            import time
            time.sleep(1.5)
            pyautogui.write(auto_type)
            if auto_enter:
                pyautogui.press('enter')
    
    else:
        result = f'{BASE_PATH}/err?msg=Cannout launch "{path}".'
    
    return result

@DevTool('/:run_shortcut')
def _handle_run_shortcut(menu_path: str) -> str:
    args = get_args_from_path(menu_path)
    path = args.get('path')
    
    if run_shortcut(path):
        result = BASE_PATH
    else:
        result = f'{BASE_PATH}/err?msg=Cannout launch "{path}".'
    
    return result
