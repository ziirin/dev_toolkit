import os
from pathlib import Path
import datetime

from src.dev_toolkit.modules.icons.icons import render_html_icon_list
from src.dev_toolkit.cli_menu.validators import FileValidator, NotFileOrFolderValidator
from src.dev_toolkit.modules.backup.backup import create_backup
from src.dev_toolkit.modules.platform_changer import platform_changer
from src.dev_toolkit.cli_menu.routing import DevTool
from src.dev_toolkit.misc import get_args_from_path
from src.dev_toolkit.cli_menu.menu import BASE_PATH, prompt
from src.dev_toolkit.config.app_config import APP_CONFIG, APP_PATHS
from src.dev_toolkit.modules.tsilang.clear_translations import remove_translation_data
from src.dev_toolkit.misc.launcher import open_url, run_bat_script, run_exe_detached, run_exe_script, run_ps_script
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
        r'c:\Fuentes\Nucleo\ShoeData'
        r'c:\Fuentes\Nucleo\Nucleo',
        r'c:\Fuentes\Nucleo\3DPlus',
        r'c:\Fuentes\Nucleo\Forma3D',
        r'c:\Fuentes\Nucleo\Foot3D',
        r'c:\Fuentes\Nucleo\ICadNest'
    ]
    
    success = True
    for project in projects:
        success &= run_exe_script(APP_PATHS.get('SAVE_SILS'), [project])
        
    result = BASE_PATH
    if success:
        result += '/success?msg=Saved translations.'
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
            
            str(Path('c:/fuentes/nucleo/nucleo/app/miscellaneous')),
            str(Path('c:/fuentes/nucleo/3dplus/app/miscellaneous')),
            str(Path('c:/fuentes/nucleo/forma3d/app/miscellaneous')),
            str(Path('c:/fuentes/nucleo/foot3d/app/miscellaneous')),
            str(Path('c:/fuentes/nucleo/icadnest/app/miscellaneous')),
            
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
        
        values = dict.fromkeys(cbproj_folders, ['w32', 'release'])
        for value in values:
            if value.lower() in debug_projects:
                values[value] = ['w32', 'debug']
        
    elif preset == 'release':
        values = dict.fromkeys(cbproj_folders, ['w64', 'release'])
    
    if len(values) > 0:
        platform_changer(values, True)
        result =  f'{BASE_PATH}/success?msg=Platform succesfully changed.'
    else:
        result =  f'{BASE_PATH}/err?msg=No project folder found.'
        
    return result

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

# ========================================================================

@DevTool('/:backup')
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
    
    if run_exe_detached(path):
        result = BASE_PATH
    else:
        result = f'{BASE_PATH}/err?msg=Cannout launch "{path}".'
    
    return result

