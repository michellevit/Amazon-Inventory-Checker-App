@echo off
SETLOCAL

REM Ensure the script is run from the project root directory
cd /d "%~dp0"

REM Delete existing build directories
echo Cleaning up old builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Build the application with PyInstaller
echo Building the application...
pyinstaller --onefile --icon=resources\app_icon.ico file_processor.py

REM PRODUCTION NOTE!!!!!!
REM When preparing for production suppress the console log / print statements by adding the windowed flag: 
REM pyinstaller --onefile --windowed --icon=resources\app_icon.ico file_processor.py

echo Build complete. Executable can be found in the dist directory.

ENDLOCAL
pause

