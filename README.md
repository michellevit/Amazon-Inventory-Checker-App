# Amazon Inventory Checker App


![Python Version](https://img.shields.io/badge/Python-3.10.4-ffdb4f.svg)
![openpyxl](https://img.shields.io/badge/OpenPyXL-3.0.9-206e47.svg)
![Tkinter](https://img.shields.io/badge/Tkinter-3A77A8.svg)


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
- Tkinter
- OpenPyXL Library


## How To Install the Program<a name="how-to-install"></a>
- to do


## How To Use the Program<a name="how-to-use"></a>
- to do


## How To Edit the Program<a name="how-to-edit"></a>
- After making code changes to file_processor.py - run: 
  - `.\rebuild-app.bat`
  - Note: The virtual environment must be created and activated:
    - To create the program follow [How To Create The Virtual Environment](#how-to-venv)
    - Open a terminal and navigate to the project's root dir 
    - Run: `.\venv\Scripts\activate`
- To run the app form the command line (to see print statements): 
  - `.\dist\file_processor.exe`


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
- Make sure app is closed before running `.\rebuild-app`


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
