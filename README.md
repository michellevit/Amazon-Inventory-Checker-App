# Amazon Inventory Checker App


![Python Version](https://img.shields.io/badge/Python-3.10.4-ffdb4f.svg)
![Tkinter](https://img.shields.io/badge/Tkinter-8.6-3A77A8.svg)
![openpyxl](https://img.shields.io/badge/OpenPyXL-3.1.2-206e47.svg)
![PyInstaller](https://img.shields.io/badge/PyInstaller-6.6.0-8CA1AF.svg)


An application that intakes an Amazon order request spreadsheet, calculates the total requested inventory, allows users to input their actual inventory, and calculates the optimal orders to confirm based on inventory and the minimum order value threshold (to keep shipping costs reasonable).


## Table of Contents
- [Technologies Used](#technologies-used)
- [How To Install the Program](#how-to-install)
- [How To Use the Program](#how-to-use)
- [How To Edit the Program](#how-to-edit)
- [How To Create a Virtual Environment](#how-to-venv)
- [Troubleshooting](#troubleshooting)
- [To Do](#to-do)
- [Credits](#credits)


## Technologies Used<a name="technologies-used"></a>
- Python (3.10.0)
- Tkinter (8.6)
- OpenPyXL Library (3.1.2)
- PyInstaller (6.6.0)


## How To Install the Program<a name="how-to-install"></a>
- Open the GitHub and save the project into a folder
- Open the app-build.bat and make sure the DEBUG value is set to FALSE
- Run the file 'app-installer.bat' to create a Desktop shortcut for the program


## How To Use the Program<a name="how-to-use"></a>
- TO DO


## How To Edit the Program<a name="how-to-edit"></a>
- Open the app-build.bat and change DEBUG value to TRUE (to see print statements)
- After making code changes to file_processor.py - run: 
  - `.\app-build.bat`
  - Note: The virtual environment must be created and activated:
    - To create the virtual environment:
      - Ensure Python3 is installed on your system
      - Open a terminal
      - Navigate to project's root directory
      - Run: `python -m venv venv`
      - Run: `pip install -r requirements.txt`
    - To activate the virtual environment: `.\venv\Scripts\activate`
      - Open a terminal and navigate to the project's root dir 
      - Run: `.\venv\Scripts\activate`
- To run the app form the command line: 
  - `.\AmazonChecker.exe


## How To Create a Virtual Environment<a name="how-to-venv"></a>
* Note: this is needed for editing the program, not running the program.
- Ensure Python is installed on your system
- Open a terminal
- Navigate to project's root directory
- Run: `python -m venv venv`
- Activate the virtual environment: `.\venv\Scripts\activate`
- If you have a requirements.txt file:
  - Run: `pip install -r requirements.txt`


## Troubleshooting<a name="troubleshooting"></a>
- Make sure app is closed before running `.\app-build`


## To Do<a name="troubleshooting"></a>
- How to install instructions
- How to use instructions


## Credits<a name="credits"></a>
Michelle Flandin



Project Directory:
Amazon-Inventory-Checker-App
| - build/
| - dist/
| | - file_processor
| - processing
| - resources
| | - app_icon.ico
| - uploaded_files/
| - venv/
| - file_processor.py
| - file_processor.spec
| - requirements.txt
