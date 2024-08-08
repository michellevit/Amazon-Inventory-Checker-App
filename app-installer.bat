@echo off
SETLOCAL

REM Ensure the script is run from the project root directory
cd /d "%~dp0"

REM Define the target installation directory (customize as needed)
set INSTALL_DIR="%USERPROFILE%\AmazonChecker"

REM Create the installation directory if it doesn't exist
if not exist %INSTALL_DIR% (
    mkdir %INSTALL_DIR%
)

REM Copy the executable and other necessary files to the installation directory
echo Setting up AmazonChecker...
copy "AmazonChecker.exe" %INSTALL_DIR%
xcopy "resources" %INSTALL_DIR%\resources /E /I /Y
copy "min_order_value.json" %INSTALL_DIR%

REM Create a shortcut to the executable on the desktop
echo Creating desktop shortcut...
set SHORTCUT_PATH="%USERPROFILE%\Desktop\Amazon Checker.lnk"
powershell -command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%SHORTCUT_PATH%');$s.TargetPath='%INSTALL_DIR%\AmazonChecker.exe';$s.IconLocation='%INSTALL_DIR%\resources\app_icon.ico';$s.WorkingDirectory='%INSTALL_DIR%';$s.Save()"

REM Clear the terminal
cls

REM Display final message
echo App installation complete. A new shortcut has been added to your desktop for the 'Amazon Checker' program!

ENDLOCAL
pause
