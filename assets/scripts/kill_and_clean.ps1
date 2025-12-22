# Define la ruta base
$TARGET_DIR = "C:\Fuentes\Nucleo"
$PROGRESS = 0

# Check if directory exists
if (!(Test-Path -Path $TARGET_DIR -PathType Container)) {
    Write-Host "Error: Could not open directory $TARGET_DIR"
    exit 1
}

# Set target directory
Set-Location -Path $TARGET_DIR
Write-Host "Target directory: $TARGET_DIR"

# Extensions to remove list
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
    "*.`$`$`$",
    "*.@@@",
    "*.~*",
    "*.twopts"
)

# Update progress [1]
Write-Host "Progress:$(++$PROGRESS)"


# Remove files with listed extensions
foreach ($ext in $extensions) {
    Write-Host "Deleting $ext..."
    Get-ChildItem -Path $ext -File -Recurse -ErrorAction SilentlyContinue | Remove-Item -Force

    # Update progress [2-18]
    Write-Host "Progress:$(++$PROGRESS)"
}

# Remove 3DPlus/obj/Win32 folder
$OBJ_DIR = Join-Path (Split-Path $TARGET_DIR -Parent) "Nucleo\3DPlus\obj\Win32"
if (Test-Path -Path $OBJ_DIR -PathType Container) {
    Write-Host "Removing directory: $OBJ_DIR"
    Remove-Item -Path $OBJ_DIR -Recurse -Force
}

# Update progress [19]
Write-Host "Progress:$(++$PROGRESS)"

# Remove Forma3D/obj/Win32 folder
$OBJ_DIR = Join-Path (Split-Path $TARGET_DIR -Parent) "Nucleo\Forma3D\obj\Win32"
if (Test-Path -Path $OBJ_DIR -PathType Container) {
    Write-Host "Removing directory: $OBJ_DIR"
    Remove-Item -Path $OBJ_DIR -Recurse -Force
}

# Update progress [20]
Write-Host "Progress:$(++$PROGRESS)"

# Kill mtbcc32exc.exe processes
Get-Process -Name "mtbcc32exc" -ErrorAction SilentlyContinue | ForEach-Object {
    Stop-Process -Id $_.Id -Force
}

# Update progress [21]
Write-Host "Progress:$(++$PROGRESS)"
Write-Host "Process completed."
