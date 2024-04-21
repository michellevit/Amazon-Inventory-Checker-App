# step_1_scripts.py

import xlrd
from openpyxl.workbook import Workbook
import os
import pyperclip
from tkinter import messagebox


def convert_xls_to_xlsx(original_path):
    book_xls = xlrd.open_workbook(original_path)
    book_xlsx = Workbook()
    sheet_xls = book_xls.sheet_by_name('Line Items')
    sheet_xlsx = book_xlsx.active
    sheet_xlsx.title = 'Line Items'
    for row in range(sheet_xls.nrows):
        for col in range(sheet_xls.ncols):
            sheet_xlsx.cell(row=row + 1, column=col + 1).value = sheet_xls.cell_value(row, col)
    return book_xlsx


def check_file_valid(workbook):
    if 'Line Items' in workbook.sheetnames:
        sheet = workbook['Line Items']
        if sheet['A3'].value == 'Order/PO Number':
            return True
        else:
            return False
    else:
        return False
    

def calculate_inventory(workbook):
    requested_inventory = {}
    sheet = workbook['Line Items']

    currency_code = sheet['U4'].value
    if currency_code == 'GENLY':
        currency = 'USD'
    elif currency_code == 'GEPQH':
        currency = 'CAD'
    else:
        currency = 'Unknown'

    for row in range(4, sheet.max_row + 1):
        model_number = sheet[f'C{row}'].value
        quantity_ordered = sheet[f'J{row}'].value

        # Stop processing if the row is empty
        if not model_number or quantity_ordered is None:
            break
        
        # Attempt to convert quantity ordered to an integer
        try:
            quantity_ordered = int(float(quantity_ordered))
        except ValueError:
            # Handle the case where conversion is not possible
            print(f"Cannot convert quantity ordered to int for row {row}.")
            continue 

        # Ensure that quantity ordered is an integer
        quantity_ordered = int(quantity_ordered)

        if model_number in requested_inventory:
            requested_inventory[model_number] += quantity_ordered
        else:
            requested_inventory[model_number] = quantity_ordered

    return requested_inventory, currency


def copy_to_clipboard(currency, inventory_dict):
    if currency == "USD":
        vendor = "Amazon US"
    elif currency == "CAD":
        vendor = "Amazon CA"
    else:
        vendor = "Amazon"

    clipboard_text = f"{vendor} - Requested Items:\n" 
    lines = [f"{model}: {quantity}" for model, quantity in inventory_dict.items()]
    clipboard_text += "\n".join(lines) 
    pyperclip.copy(clipboard_text)
    messagebox.showinfo("Clipboard", "Inventory data copied to clipboard!")