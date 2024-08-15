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
- Open the app-builder.bat and make sure the DEBUG value is set to FALSE
- Run the file 'app-installer.bat' to create a Desktop shortcut for the program


## How To Use the Program<a name="how-to-use"></a>
- TO DO


## How To Edit the Program<a name="how-to-edit"></a>
- Open the app-builder.bat and change DEBUG value to TRUE (to see print statements)
- After making code changes to file_processor.py - run: 
  - `.\app-builder.bat`
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
- To run the app form the command line: 
  - `.\AmazonChecker.exe


## Troubleshooting<a name="troubleshooting"></a>
- Make sure app is closed before running `.\app-builder`
- If app-builder.bat encounters the error `Operation did not complete successfully because the file contains a virus or potentially unwanted software.`
  - This occurs due to pyinstaller being seen as a threat, so you must exclude the dir where you are building the executable from the antivirus software:
    - Open Windows Security.
    - Go to "Virus & threat protection."
    - Click on "Manage settings" under Virus & threat protection settings.
    - Scroll down to "Exclusions" and click on "Add or remove exclusions."
    - Click "Add an exclusion" and select "Folder," then navigate to your project directory.


## To Do<a name="troubleshooting"></a>
- store all the accepted inventory (available inventory from the form) in a dict
- after the second PASS go through and get the confirmed_inventory dict
- create a new dict called extra_inventory
- if there is extra_inventory:
  - step 1:
    - create a new dict called accepted_orders with orders that have been accepted
      - if any of the accepted orders have cancelled units and there are units in extra_inventory fill
      - fill until either is full/empty
  - step 2:
    - if there is still extra_inventory:
      - go through non_accepted orders
      - go through the entire order and fill it up with extra_inventory
      - if the order goes over min_order_val
- go through all the orders which
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
