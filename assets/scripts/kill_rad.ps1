# Matar procesos mtbcc32exc.exe
Get-Process -Name "mtbcc32exc" -ErrorAction SilentlyContinue | ForEach-Object {
    Stop-Process -Id $_.Id -Force
}

Write-Host "Proceso completado."