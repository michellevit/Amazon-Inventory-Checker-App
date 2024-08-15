@echo off
SETLOCAL

REM Ensure the script is run from the project root directory
cd /d "%~dp0"

REM Dynamically determine the installation directory based on where the script is executed
set INSTALL_DIR=%~dp0

REM Create a shortcut to the executable on the desktop
echo Creating desktop shortcut...
set SHORTCUT_PATH=%USERPROFILE%\Desktop\Amazon Checker.lnk

powershell -command ^
"$s=(New-Object -COM WScript.Shell).CreateShortcut('%SHORTCUT_PATH%'); ^
$s.TargetPath='%INSTALL_DIR%AmazonChecker.exe'; ^
$s.IconLocation='%INSTALL_DIR%resources\\app_icon.ico'; ^
$s.WorkingDirectory='%INSTALL_DIR%'; ^
$s.Save()"

REM Clear the terminal (comment out for debugging)
cls

REM Display final message
echo App installation complete. A new shortcut has been added to your desktop for the 'Amazon Checker' program!

ENDLOCAL
pause
