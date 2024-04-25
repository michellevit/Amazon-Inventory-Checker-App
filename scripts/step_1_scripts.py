# step_1_scripts.py

from openpyxl.workbook import Workbook
from openpyxl import load_workbook
import os
import pyperclip
from tkinter import messagebox
import xlrd


def convert_xls_to_xlsx(original_path, currency):
    # Read the original workbook using xlrd
    book_xls = xlrd.open_workbook(original_path)
    sheet_xls = book_xls.sheet_by_name('Line Items')
    # Create a new workbook using openpyxl
    book_xlsx = Workbook()
    sheet_xlsx = book_xlsx.active
    sheet_xlsx.title = 'Line Items'
    # Copy data from the old xls file to the new xlsx file
    for row in range(sheet_xls.nrows):
        for col in range(sheet_xls.ncols):
            sheet_xlsx.cell(row=row + 1, column=col + 1, value=sheet_xls.cell_value(row, col))
    # Generate new filename with '- Complete 1' suffix
    directory, filename = os.path.split(original_path)
    filename_without_extension, _ = os.path.splitext(filename)
    capitalized_currency = currency.upper()
    new_filename = f"{filename_without_extension} - {capitalized_currency} Complete 1.xlsx"
    new_file_path = os.path.join(directory, new_filename)
    # Save the new workbook in the same directory as the original
    book_xlsx
    # Return the new workbook object
    return book_xlsx, new_filename,new_file_path

def create_new_file(original_path, currency):
    workbook = load_workbook(original_path)
    if 'Line Items' not in workbook.sheetnames:
        raise ValueError("No 'Line Items' sheet found in the workbook.")
    original_sheet = workbook['Line Items']
    new_workbook = load_workbook()
    new_sheet = new_workbook.active
    new_sheet.title = 'Line Items'
    for row in original_sheet.iter_rows():
        for cell in row:
            new_cell = new_sheet.cell(row=cell.row, column=cell.column, value=cell.value)
    directory, filename = os.path.split(original_path)
    filename_without_extension, _ = os.path.splitext(filename)
    capitalized_currency = currency.upper()
    new_filename = f"{filename_without_extension} - {capitalized_currency} Complete 1.xlsx"
    new_file_path = os.path.join(directory, new_filename)
    
    new_workbook.save(new_file_path)
    return new_workbook, new_filename, new_file_path



def check_file_valid(workbook, currency):
    capitalized_currency = currency.upper()
    if 'Line Items' not in workbook.sheetnames:
        raise ValueError("The file entered is not valid (it does not have a 'Line Items' tab).")
    sheet = workbook['Line Items']
    if capitalized_currency not in sheet['AF4'].value:
        raise ValueError(f"Please enter the {capitalized_currency} into the correct input.")
    return True


def cancel_orders_below_min(workbook, min_order_value, new_file_path, po_value_dict):
    sheet = workbook['Line Items']
    for row in range(4, sheet.max_row + 1):
        if not sheet[f'A{row}'].value:
            break
        order_number = sheet[f'A{row}'].value
        quantity_ordered = sheet[f'J{row}'].value # Type = float
        item_cost = sheet[f'I{row}'].value # Type = float
        line_item_value = quantity_ordered * item_cost
        if order_number in po_value_dict:
            po_value_dict[order_number] = po_value_dict[order_number] + line_item_value
        else:
            po_value_dict[order_number] = line_item_value
    orders_to_cancel_array = []
    for key, value in po_value_dict.items():
        if value < int(min_order_value.get()):
            orders_to_cancel_array.append(key)
    for key in po_value_dict:
        if key in orders_to_cancel_array:
            po_value_dict[key] = 0.0
    for row in range(4, sheet.max_row + 1):
        if not sheet[f'A{row}'].value:
            break
        if order_number in orders_to_cancel_array:
            sheet[f'L{row}'].value = 0.0
            sheet[f'S{row}'].value = "CA - Cancelled: Not yet available"
    print("PO Value Dict: ", po_value_dict)
    print("Orders to cancel: ", orders_to_cancel_array)
    # This is wrong !!!!!!!!!!!!!!!!!!!!!!!!
    workbook.save(new_file_path)
    return workbook



def calculate_inventory(workbook, requested_inventory):
    sheet = workbook['Line Items']
    for row in range(4, sheet.max_row + 1):
        model_number = sheet[f'C{row}'].value
        quantity_ordered = sheet[f'L{row}'].value
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