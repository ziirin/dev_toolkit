import subprocess
import webbrowser
from pathlib import Path

def open_url(url: str) -> bool:
    try:
        webbrowser.open(url)
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