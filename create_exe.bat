pyinstaller --noconfirm --onefile --console --distpath . --paths "." main.py

copy /Y .\main.exe c:\copias\todos
robocopy .\assets c:\copias\todos\assets /MIR /Z /R:3 /W:5