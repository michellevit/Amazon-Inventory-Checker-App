REM app-build.bat

REM This script should be run when a change is made to any of the code

@echo off
SETLOCAL

REM Define DEBUG variable (set to TRUE for debugging, FALSE for production)
REM Toggles whether to show print statements for debugging
SET DEBUG=False

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

REM Rename the executable
echo Renaming the executable...
move "dist\file_processor.exe" "AmazonChecker.exe"

echo Build complete. Executable has been renamed.

ENDLOCAL
pause
