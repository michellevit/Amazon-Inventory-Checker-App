# Amazon Inventory Checker App


![Django Version](https://img.shields.io/badge/Django-4.0.3-0c4a30.svg)
![Python Version](https://img.shields.io/badge/Python-3.10.4-ffdb4f.svg)
![Tkinter](https://img.shields.io/badge/Tkinter-3A77A8.svg)
![React Version](https://img.shields.io/badge/React-18.2.0-61dafb.svg)


An application that intakes an Amazon order request spreadsheet, calculates the total requested inventory, allows users to input their actual inventory, and calculates the optimal orders to confirm based on inventory and the minimum order value threshold (to keep shipping costs reasonable).


## Table of Contents
- [Technologies Used](#technologies-used)
- [How to Use](#how-to-use)
- [How to Create a Virtual Environment](#how-to-venv)
- [Troubleshooting](#troubleshooting)
- [To Do](#to-do)
- [Credits](#credits)


## Technologies Used<a name="technologies-used"></a>
- Python (3.10.0)
- Tkinter
- OpenPyXL Library


## How to Use<a name="how-to-use"></a>
- After making code changes to file_processor.py - run: 
  - `.\rebuild-app.bat`
- To run the app form the command line: 
  - `.\dist\file_processor.exe`


## How to Create a Virtual Environment<a name="how-to-venv"></a>
- Ensure Python is installed on your system
- Open a terminal
- Navigate to project's root directory
- Run: `python -m venv venv`
- Activate the virtual environment: `.\venv\Scripts\activate`
- If you have a requirements.txt file:
  - Run: `pip install -r requirements.txt`


## Troubleshooting<a name="troubleshooting"></a>
- Make sure app is closed before running `.\rebuild-app`


## To Do<a name="to-do"></a>
- CASES:
  - 1 file entered with requested items, must be submitted
  - 1 file entered with no requested items, nothing to submit
  - 1 file entered, but all below threshold -> submit empty form

  - 2 files entered both with requested items, both must be submitted 
  - 2 files entered both with no requested items, nothing to submit
  - 2 files entered, all below threshold -> submit empty forms
  - 2 files entered, 1 is empty so nothing to submit, 1 must be submitted
  - 2 files entered, 1 is empty so nothing to submit, 1 is all below threshold so must submit

- First pass: 
  - loop both sheets (new sheets): us sheet + ca sheet:
    - for each line item, if model_number in items_to_cancel dict
      - yes: 
        - create var: model_number
        - create var: order_number
        - create var: quantity_confirmed (col L)
        - create var one_unit_cost (col I)
        - create var: min_order_value for that currency
        - create var order_value[model_number]
        - remove 1 unit cost from the new order_value var
        - while quantity_confirmed > 0 and items_to_cancel[model_number] > 0 and order_value_var_ not below min_threshold:
            - remove 1 unit from 'Quantity Confirmed' col
            - remove 1 unit from quantity_confirmed var
            - remove 1 unit from items_to_cancel[model_number] dict
            - remove 1 unit from order_value[order_number] dict
            - if value of items_to_cancel[model_number] is 0 then remove entry from dict
- Second pass:
  - loop both sheets (new sheets): us sheet + ca sheet:
    - If still items in the items_to_cancel dict
    - remove entries in order_value_dict with value of zero 
    - organize order_value_dict form lowest value to highest value
    - for order in order_value_dict:
      - for each line in sheet, if it matches the order number:
        - check if the model_number is in the units_to_cancel dict:
          - yes: 
            - create var: model_number
            - create var: order_number
            - create var: quantity_confirmed (col L)
            - create var one_unit_cost (col I)
            - create var: min_order_value for that currency
            - create var order_value[model_number]
            - while quantity_confirmed > 0 and items_to_cancel[model_number] > 0: 
              - remove 1 unit from 'Quantity Confirmed' col
              - remove 1 unit from quantity_confirmed var
              - remove 1 unit from items_to_cancel[model_number] dict
              - remove 1 unit from order_value[order_number] dict
              - if value of items_to_cancel[model_number] is 0 then remove entry from dict
- Third pass: 
  - loop both sheets (new sheets): us sheet + ca sheet:
    - Tabulate new order_value_dict based on new order values
    - Tabulate a new order_to_cancel array (based on currency (col AF) min_order_value)
    - For each line item: 
      - if order_number in orders_to_cancel array:
        - yes:
          - set 'Quantity Confirmed' col quantity to 0
          - change 'Availability Status' col value to 'CA - Cancelled: Not yet available'
  - Fourth pass: 
  - convert temp sheet(s) to .xls format
  - rename file "Completed Inventory Sheet For Amazon Submission - [currency]"
  - create new message for user "Inventory reports are complete - please submit the report(s) *list report(s)* 
  to Amazon Vendor Central 
  - Replace 'Inventory Frame':
    - Columns: Model Number and Quantity Confirmed
    - remove form entry fields
    - remove submit button
    - modify copy message to: 'Amazon US/CA Confirmed Items' 
- Edge Case: no orders over min_order_value -> display_inventory_form()

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