import os
import subprocess
import webbrowser
from pathlib import Path
from datetime import (datetime, timedelta)
from .routing import DevTool
from ..misc import get_args_from_path
from ..cli_menu.menu import (BASE_PATH, prompt)
from ..modules.tsilang.clear_translations import remove_translation_data
from .validators import (FirstDayOfWeekValidator,
                         ProjectNameValidator,
                         BoolValidator,
                         RemainingTimeValidator,
                         NumberValidator)
from ..modules.tsilang.silFixer import (read_sil,
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
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            csv_data = read_csv(input_path)[0]
            write_sil(output_path, csv_data)
            result += f'/success?msg=File succesfully converted ({output_path}).'
        except Exception as e:
            result += f'/err?{e}'
    else:
        result += f'/err?msg=Following file doesnt exists: {input_path}.'

    return result

@DevTool('/tsilang/:clear')
def _handle_clear(menu_path: str) -> str:
    args = get_args_from_path(menu_path)
    result = BASE_PATH
    
    path = args.get('path', '')
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
        
# ========================================================================

@DevTool('/:week_report')
def _handle_week_report(menu_path: str) -> str:
    data = {
        'cur_week_begin': '',
        'next_week_begin': '',
        'cur_week_projects': {},
        'next_week_projects': {},
        'variance_projects': {}
    }
    
    now = datetime.now()
    curr_monday = now - timedelta(days=now.weekday())
    next_monday = curr_monday + timedelta(days=7)
    data['cur_week_begin'] = prompt('First day of current week: ',
                                    validator=FirstDayOfWeekValidator(),
                                    default=curr_monday.strftime('%d/%m'))
    data['next_week_begin'] = next_monday
    
    add_another = 'y'
    while add_another in BoolValidator.TRUE_VALUES:
        project_name = prompt('Project name: ', validator=ProjectNameValidator())
        ticket_num = prompt('T#', placeholder='0000', validator=NumberValidator())
        description = prompt('Description: ')
        remaining = prompt('Tiempo restante: ', validator=RemainingTimeValidator())
        add_another = prompt('¿Añadir otro? (y/n)', validator=BoolValidator())
        
        if project_name not in data['cur_week_projects'].keys():
            data['cur_week_projects'][project_name] = []
        description = f'T#{ticket_num} - {description}' if ticket_num else description
        data['cur_week_projects'][project_name].append({
            'description': description,
            'remaining': RemainingTimeValidator.value_to_str(remaining)
        })
        
# ========================================================================

@DevTool('/:calculahora')
def _handle_calculahora(menu_path: str) -> str:
    CALCULAHORA_PATH = Path('./assets/templates/calculahora.html').resolve()
    result = BASE_PATH
    
    if os.path.isfile(CALCULAHORA_PATH):
        webbrowser.open(f'file://{CALCULAHORA_PATH}')
    else:
        result += f'/err?msg=File "{CALCULAHORA_PATH}" not found.'
    return result