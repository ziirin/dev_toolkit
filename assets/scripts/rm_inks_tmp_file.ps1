if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Start-Process powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    Exit
}

$USER = $env:USERNAME
Remove-Item -Path "c:\Users\$USER\AppData\Local\recently-used.xbel" -Force -ErrorAction SilentlyContinue