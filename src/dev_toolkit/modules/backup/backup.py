import os
import subprocess
from pathlib import Path

def create_backup(src_folder: str, rar_file: str) -> bool:
    # os.makedirs(rar_file, exist_ok=True)
    winrar_exe = Path('c:/program files/winrar/rar.exe')
    
    extensions = ['*.cbproj', '*.h', '*.cpp', '*.c', '*.groupproj', '*.sil', '*.rh',
                '*.dfm', '*.silproj', '*.hpp', '*.cc', '*.rc', '*.ico', '*.ini']
    inclusions = [f'-n{Path(src_folder) / ext}' for ext in extensions]
    winrar_args = [
        winrar_exe, 'a', '-r', '-m5', '-ibck',
        rar_file,
        '-x*\\__astcache', '-x*\\__recovery', '-x*\\__history'
    ] + inclusions + [src_folder]
    
    try:
        process = subprocess.Popen(
            winrar_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=src_folder,
            bufsize=1
        )
        
        for line in process.stdout:
            print(f'[BACKUP]: {line.strip()}')
            
        process.wait()
        return (process.returncode == 0)
    except:
        return False