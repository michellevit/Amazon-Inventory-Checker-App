# Amazon Inventory Checker App


![Python Version](https://img.shields.io/badge/Python-3.10.4-ffdb4f.svg)
![Tkinter](https://img.shields.io/badge/Tkinter-8.6-3A77A8.svg)
![openpyxl](https://img.shields.io/badge/OpenPyXL-3.1.2-206e47.svg)
![PyInstaller](https://img.shields.io/badge/PyInstaller-6.6.0-8CA1AF.svg)


An application that intakes an Amazon order request spreadsheet, calculates the total requested inventory, allows users to input their actual inventory, and calculates the optimal orders to confirm based on inventory and the minimum order value threshold (to keep shipping costs reasonable).


<a href="https://youtu.be/WcHKO0UPXGo?si=MWx0eaWaXHBHora6" target="_blank"><img src="https://img.shields.io/badge/YouTube-Demo-red?style=for-the-badge&logo=youtube&color=FF0000"></a>


## Table of Contents
- [Technologies Used](#technologies-used)
- [How To Install the Program](#how-to-install-the-program)
- [How To Edit the Program](#how-to-edit-the-program)
- [Troubleshooting](#troubleshooting)
- [To Do](#to-do)
- [Credits](#credits)


## Technologies Used<a name="technologies-used"></a>
- Python (3.10.0)
- Tkinter (8.6)
- OpenPyXL Library (3.1.2)
- PyInstaller (6.6.0)


## How To Install the Program
* Note: these instructions are intended for users who are using the app, but not editing the app
  * Editing the app requires cloning a local copy of repo, installing Python, and creating/activating a virtual environment
- Open the [project's GitHub repository](https://github.com/michellevit/Amazon-Inventory-Checker-App)
- Select the green 'Code' button, and select 'Download ZIP'
- Find the newly downloaded zip folder (in the Download tab, select 'Show in folder')
- Right click the .zip folder, click 'Extract All...', and select the desired destination folder for the application
   - Note: make sure to save the folder directly onto your personal computer, not on a remote server (due to necessary file permissions).
- Open the unzipped folder and double-click the 'app-installer.bat' file
  - A new shortcut will be created on the Desktop for the application
  - Note: if you move the location of the application folder, you will need to delete the shortcut and run 'app-installer.bat' again


## How To Edit the Program<a name="how-to-edit"></a>
- Open the app-builder.bat and change DEBUG value to TRUE (to see print statements)
- Activate the Virtual Terminal - run: `.\venv\Scripts\activate`
- After making code changes to the code - run: `.\app-builder.bat`
- Run the app from the command line to see print statements in the terminal: `.\AmazonChecker.exe`
- Troubleshooting Notes:
  - Note 1: For unsuccessful build issues, see [Troubleshooting section](#troubleshooting)
  - Note 2: The virtual environment must be created and activated to run the build script (but not 
    needed for running the program itself due to pyinstaller):
      - To create the virtual environment:
        - Ensure Python3 is installed on your system
        - Open a terminal
        - Navigate to project's root directory
        - Run: `python -m venv venv`
        - Run: `pip install -r requirements.txt`
      - To activate the virtual environment:
        - Open a terminal and navigate to the project's root dir 
        - Run: `.\venv\Scripts\activate`
  - Note 3: After the program is done being edited, open the app-builder.bat and make sure the DEBUG value is set to FALSE and run the app-builder again


## Troubleshooting<a name="troubleshooting"></a>
- If `.\app-builder` does not work:
  - Make sure the app is closed and the spreadsheets being used are closed
- If app-builder.bat encounters the error `Operation did not complete successfully because the file contains a virus or potentially unwanted software.`:
  - This occurs due to pyinstaller being seen as a threat, so you must exclude the dir where you are building the executable from the antivirus software:
    - Open Windows Security.
    - Go to "Virus & threat protection."
    - Click on "Manage settings" under Virus & threat protection settings.
    - Scroll down to "Exclusions" and click on "Add or remove exclusions."
    - Click "Add an exclusion" and select "Folder," then navigate to your project directory.
- If the minimum order value is having issues or if you move the location of the application folder:
  - Delete the app shortcut and run 'app-installer.bat' again
- If the terminal opens after starting the program:
  - Make sure the DEBUG value is set to FALSE in app-builder.bat


## Credits<a name="credits"></a>
Michelle Flandin