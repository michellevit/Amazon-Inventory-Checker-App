# Amazon Inventory Checker App

![Django Version](https://img.shields.io/badge/Django-4.0.3-0c4a30.svg)
![Python Version](https://img.shields.io/badge/Python-3.10.4-ffdb4f.svg)
![React Version](https://img.shields.io/badge/React-18.2.0-61dafb.svg)


An application that intakes an Amazon order request spreadsheet, calculates the total requested inventory, allows users to input their actual inventory, and calculates the optimal orders to confirm based on inventory and the minimum order value threshold (to keep shipping costs reasonable).

## Table of Contents
- [How to Use](#how-to-use)
- [How to Create a Virtual Environment](#how-to-venv)



## How to Use<a name="how-to-use"></a>
- After making code changes to file_processor.py - run: 
  - `.\rebuild-app.bat
`

## How to Create a Virtual Environment<a name="how-to-venv"></a>
- Ensure Python is installed on your system
- Open a terminal
- Navigate to project's root directory
- Run: `python -m venv venv`
- Activate the virtual environment: `.\venv\Scripts\activate`
- If you have a requirements.txt file:
  - Run: `pip install -r requirements.txt`


Project Directory:
Amazon-Inventory-Checker-App
| - build/
| - dist/
| | - file_processor
| - resources
| | - app_icon.ico
| - uploaded_files/
| - venv/
| - file_processor.py
| - file_processor.spec
| - requirements.txt

