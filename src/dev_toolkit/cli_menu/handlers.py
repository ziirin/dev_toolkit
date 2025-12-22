import os
import subprocess
from .routing import DevTool
from ..misc import get_args_from_path
from ..cli_menu.menu import BASE_PATH
from ..modules.sil_fixer.silFixer import (read_sil,
                                          write_sil,
                                          read_csv,
                                          write_csv)

# ========================================================================

@DevTool('/tsilang/:sil2csv')
def _handle_sil2csv(menu_path: str) -> str:
    args = get_args_from_path(menu_path)
    result = BASE_PATH
    
    input_path = args.get('in', '')
    output_path = args.get('out', '')
    if os.path.isfile(input_path):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        sil_data = read_sil(input_path)[0]
        write_csv(output_path, sil_data)
        result += f'/success?msg=File succesfully converted ({output_path}).'
    else:
        result += f'/err?msg=Following file doesnt exists: {input_path}.'

    return result

@DevTool('/tsilang/:csv2sil')
def _handle_csv2sil(menu_path: str) -> str:
    args = get_args_from_path(menu_path)
    result = BASE_PATH
    
    input_path = args.get('in', '')
    output_path = args.get('out', '')
    if os.path.isfile(input_path):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        csv_data = read_csv(input_path)[0]
        write_sil(output_path, csv_data)
        result += f'/success?msg=File succesfully converted ({output_path}).'
    else:
        result += f'/err?msg=Following file doesnt exists: {input_path}.'

    return result

# ========================================================================

@DevTool('/:kill_rad')
def _handle_kill_rad(menu_path: str) -> str:
    KILL_RAD_PATH = './assets/kill_and_clean.ps1'
    result = BASE_PATH
    
    if os.path.isfile(KILL_RAD_PATH):
        process = subprocess.run(
            ['powershell.exe', '-ExecutionPolicy', 'Bypass', '-File', KILL_RAD_PATH],
            capture_output=True,
            text=True,
            check=True
        )
                
        if process.returncode == 0:
            result += f'/success?msg=RAD Studio cleaned and killed.'
        else:
            result += f'/err?msg=An error occurred.'
    else:
        result += f'/err?msg=Script "{KILL_RAD_PATH}" not found.'