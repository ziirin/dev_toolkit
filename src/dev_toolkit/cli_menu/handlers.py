import os
from pathlib import Path
import subprocess

from src.dev_toolkit.cli_menu.routing import DevTool
from src.dev_toolkit.misc import get_args_from_path
from src.dev_toolkit.cli_menu.menu import BASE_PATH
from src.dev_toolkit.config.app_config import APP_CONFIG, APP_PATHS
from src.dev_toolkit.modules.tsilang.clear_translations import remove_translation_data
from src.dev_toolkit.misc.launcher import open_url, run_bat_script, run_exe_script, run_ps_script
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
def handle_load_sil(menu_path: str) -> str:
    result = BASE_PATH
    if run_bat_script(APP_PATHS.get('LOAD_SILS')):
        result += f'/success?msg=Translations loaded.'
    else:
        result += f'/err?msg=An error occurred.'
        
    return result

@DevTool('/tsilang/:save')
def handle_save_sil(menu_path: str) -> str:
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

@DevTool('/:kill_rad')
def _handle_kill_rad(menu_path: str) -> str:
    KILL_RAD_PATH = './assets/scripts/kill_and_clean.ps1'
    result = BASE_PATH
    
    if run_ps_script(KILL_RAD_PATH):
        result += f'/success?msg=RAD Studio cleaned and killed.'
    else:
        result += f'/err?msg=An error occurred.'
    
    return result
        
# ========================================================================

@DevTool('/:calculahora')
def _handle_calculahora(menu_path: str) -> str:
    CALCULAHORA_URL = 'https://tickets.inescop.es/horas.html'
    
    if open_url(CALCULAHORA_URL):
        result = BASE_PATH
    else:
        result = f'{BASE_PATH}/err?msg=Cannout launch "{CALCULAHORA_URL}".'
    
    return result

# ========================================================================

@DevTool('/common_links/:ticket_platform')
def _handle_ticket_platform(menu_path: str) -> str:
    TICKET_PLATFORM_URL = 'https://tickets.inescop.es/scp/index.php'
    
    if open_url(TICKET_PLATFORM_URL):
        result = BASE_PATH
    else:
        result = f'{BASE_PATH}/err?msg=Cannout launch "{TICKET_PLATFORM_URL}".'
    
    return result

@DevTool('/common_links/:ia_gpt')
def _handle_ticket_platform(menu_path: str) -> str:
    CHAT_GPT_URL = 'https://chatgpt.com/?temporary-chat=true'
    
    if open_url(CHAT_GPT_URL):
        result = BASE_PATH
    else:
        result = f'{BASE_PATH}/err?msg=Cannout launch "{CHAT_GPT_URL}".'
    
    return result

@DevTool('/common_links/:ia_gemini')
def _handle_ticket_platform(menu_path: str) -> str:
    GEMINI_URL = 'https://gemini.google.com/app'
    
    if open_url(GEMINI_URL):
        result = BASE_PATH
    else:
        result = f'{BASE_PATH}/err?msg=Cannout launch "{GEMINI_URL}".'
    
    return result

@DevTool('/common_links/:ia_claude')
def _handle_ticket_platform(menu_path: str) -> str:
    CLAUDE_URL = 'https://claude.ai/new'
    
    if open_url(CLAUDE_URL):
        result = BASE_PATH
    else:
        result = f'{BASE_PATH}/err?msg=Cannout launch "{CLAUDE_URL}".'
    
    return result