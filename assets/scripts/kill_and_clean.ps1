# Define la ruta base
$TARGET_DIR = "C:\Fuentes\Nucleo"

# Verifica si el directorio existe
if (!(Test-Path -Path $TARGET_DIR -PathType Container)) {
    Write-Host "Error: No se pudo acceder al directorio $TARGET_DIR"
    exit 1
}

# Cambia al directorio objetivo
Set-Location -Path $TARGET_DIR

Write-Host "Eliminando archivos con extensiones específicas en: $TARGET_DIR"

# Lista de extensiones a eliminar
$extensions = @(
    "_3DPlus.exe",
    "*.obj",
    "*.dcu",
    "*.map",
    "*.pdi",
    "*.bpi",
    "*.ilc",
    "*.ild",
    "*.ilf",
    "*.ils",
    "*.tds",
    "*.tmp",
    "*.ild",
    "*.local",
    "*.identcache",
    "*.stat",
    "*.`$`$`$",
    "*.@@@",
    "*.~*",
    "*.twopts"
)

# Eliminar archivos con las extensiones listadas
foreach ($ext in $extensions) {
    Write-Host "Eliminando $ext..."
    Get-ChildItem -Path $ext -File -Recurse -ErrorAction SilentlyContinue | Remove-Item -Force
}

# Eliminar carpeta Nucleo/obj si existe
$OBJ_DIR = Join-Path (Split-Path $TARGET_DIR -Parent) "Nucleo\Nucleo\obj"
if (Test-Path -Path $OBJ_DIR -PathType Container) {
    Write-Host "Eliminando carpeta: $OBJ_DIR"
    Remove-Item -Path $OBJ_DIR -Recurse -Force
} else {
    Write-Host "Carpeta no encontrada: $OBJ_DIR"
}

# Eliminar carpeta 3DPlus/obj si existe
$OBJ_DIR = Join-Path (Split-Path $TARGET_DIR -Parent) "Nucleo\3DPlus\obj"
if (Test-Path -Path $OBJ_DIR -PathType Container) {
    Write-Host "Eliminando carpeta: $OBJ_DIR"
    Remove-Item -Path $OBJ_DIR -Recurse -Force
} else {
    Write-Host "Carpeta no encontrada: $OBJ_DIR"
}

# Eliminar carpeta Forma3d/obj si existe
$OBJ_DIR = Join-Path (Split-Path $TARGET_DIR -Parent) "Nucleo\Forma3D\obj"
if (Test-Path -Path $OBJ_DIR -PathType Container) {
    Write-Host "Eliminando carpeta: $OBJ_DIR"
    Remove-Item -Path $OBJ_DIR -Recurse -Force
} else {
    Write-Host "Carpeta no encontrada: $OBJ_DIR"
}

# Matar procesos mtbcc32exc.exe
Get-Process -Name "mtbcc32exc" -ErrorAction SilentlyContinue | ForEach-Object {
    Stop-Process -Id $_.Id -Force
}

Write-Host "Proceso completado."
Read-Host -Prompt "Presiona ENTER para salir"
