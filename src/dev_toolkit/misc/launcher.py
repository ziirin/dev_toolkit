import os
import subprocess
import webbrowser
from pathlib import Path

def open_url(url: str, is_uri: bool = False) -> bool:
    try:
        _url = url
        if is_uri:
            _url = Path(_url)
        webbrowser.open(_url)
    except:
        return False
    return True

def run_ps_script(script_path: str) -> bool:
    try:
        if Path(script_path).is_file():
            process = subprocess.Popen(
                ['powershell.exe', '-ExecutionPolicy', 'Bypass', '-File', script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            for line in process.stdout:
                print(f'[PS1]: {line.strip()}')
            process.wait()
            return (process.returncode == 0)
        else:
            return False
    except:
        return False
    
def run_ps_command(command: list[str]) -> list[bool, str | None]:
    try:
        if command:
            process = subprocess.Popen(
                ['powershell.exe'] + command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            ret_str = ''
            for line in process.stdout:
                ret_str += line.strip()
                print(f'[PS1]: {line.strip()}')
                
            process.wait()
            return (process.returncode == 0, ret_str)
        else:
            return (False, None)
    except:
        return (False, None)
    
def run_bat_script(script_path: str) -> bool:
    try:
        if Path(script_path).is_file():
            process = subprocess.Popen(
                script_path,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            for line in process.stdout:
                print(f'[BAT]: {line.strip()}')
            process.wait()
            return (process.returncode == 0)
        else:
            return False
    except:
        return False
    
def run_exe_script(script_path: str, args: list[str] = []) -> bool:
    try:
        if Path(script_path).is_file():
            print(f'Running {Path(script_path).name} ...')
            process = subprocess.run(
                [script_path] + args,
                capture_output=True,
                text=True,
                check=True
            )
            
            print(f'[EXE]: {process.stdout}')
            return (process.returncode == 0)
        else:
            return False
    except:
        return False
    
def run_exe_detached(script_path: str, args: list[str] = []) -> bool:
    try:
        if Path(script_path).is_file():
            subprocess.Popen(
                [script_path] + args,
                creationflags=subprocess.DETACHED_PROCESS
            )
            
            return True
        else:
            return False
    except:
        return False
    
def run_shortcut(shortcut_path: str) -> bool:
    try:
        path = Path(shortcut_path)
        if path.is_file():
            os.startfile(str(path))
        else:
            return False
    except:
        return False
    
    return True