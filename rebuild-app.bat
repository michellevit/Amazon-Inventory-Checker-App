@echo off
SETLOCAL

REM Define DEBUG variable (set to TRUE for debugging, FALSE for production)
REM Toggles whether to show print statements for debugging
SET DEBUG=FALSE

REM Ensure the script is run from the project root directory
cd /d "%~dp0"

REM Delete existing build directories
echo Cleaning up old builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Build the application with PyInstaller
echo Building the application...

if "%DEBUG%"=="TRUE" (
    echo Debug mode: Building without --windowed option...
    pyinstaller --onefile --icon=resources\app_icon.ico file_processor.py
) else (
    echo Production mode: Building with --windowed option...
    pyinstaller --onefile --windowed --icon=resources\app_icon.ico file_processor.py
)

echo Build complete. Executable can be found in the dist directory.

ENDLOCAL
pause

