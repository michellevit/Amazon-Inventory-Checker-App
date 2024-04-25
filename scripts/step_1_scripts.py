# step_1_scripts.py

from openpyxl.workbook import Workbook
import pyperclip
from tkinter import messagebox
import xlrd


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


def check_file_valid(workbook, currency):
    capitalized_currency = currency.upper()
    if 'Line Items' not in workbook.sheetnames:
        raise ValueError("The file entered is not valid (it does not have a 'Line Items' tab).")
    sheet = workbook['Line Items']
    if capitalized_currency not in sheet['AF4'].value:
        raise ValueError("The file entered is not the correct currency")
    return True


def cancel_orders_below_min(workbook, min_value):
    sheet = workbook['Line Items']
    po_value_dict = {}
    for row in range(4, sheet.max_row + 1):
        if not sheet[f'A{row}'].value:
            break
        order_number = sheet[f'A{row}'].value
        quantity_ordered = sheet[f'J{row}'].value
        item_cost = sheet['I{row}'].value
        line_item_value = quantity_ordered * item_cost
        if order_number in po_value_dict:
            po_value_dict[order_number] = po_value_dict[order_number].value + line_item_value
        else:
            po_value_dict[order_number] = line_item_value
    orders_to_cancel_array = []
    for key, value in po_value_dict.items():
        if value < min_value:
            orders_to_cancel_array.append(key)
    for row in range(4, sheet.max_row + 1):
        if not sheet[f'A{row}'].value:
            break



def calculate_inventory(workbook, requested_inventory):
    sheet = workbook['Line Items']
    for row in range(4, sheet.max_row + 1):
        model_number = sheet[f'C{row}'].value
        quantity_ordered = sheet[f'J{row}'].value
        if not model_number or quantity_ordered is None:
            break
        try:
            quantity_ordered = int(float(quantity_ordered))
        except ValueError:
            print(f"Cannot convert quantity ordered to int for row {row}.")
            continue 
        quantity_ordered = int(quantity_ordered)
        if model_number in requested_inventory:
            requested_inventory[model_number] += quantity_ordered
        else:
            requested_inventory[model_number] = quantity_ordered
    requested_inventory = dict(sorted(requested_inventory.items()))
    return requested_inventory


def find_vendor_origins(submitted_files):
    if len(submitted_files) == 2:
        return "Amazon US + CA"
    elif "us" in submitted_files:
        return "Amazon US"
    else: 
        return "Amazon CA"

def copy_to_clipboard(inventory_dict, vendor_origins):
    clipboard_text = f"{vendor_origins} - Requested Items:\n" 
    lines = [f"{model}: {quantity}" for model, quantity in inventory_dict.items()]
    clipboard_text += "\n".join(lines) 
    pyperclip.copy(clipboard_text)
    messagebox.showinfo("Clipboard", "Inventory data copied to clipboard!")