# step_2_scripts.py

import pprint
import os
from openpyxl import load_workbook
from openpyxl.utils.datetime import from_excel
import xlwt


def calculate_units_to_cancel(requested_inventory, available_inventory):

    units_to_cancel = {}

    # print('\n')
    # pprint.pprint("REQUESTED INVENTORY:")
    # pprint.pprint(requested_inventory)

    # print('\n')
    # pprint.pprint("ENTRIES: ")
    # pprint.pprint(available_inventory)

    for model_number in requested_inventory:
        if requested_inventory[model_number] > available_inventory[model_number]:
            discrepancy = requested_inventory[model_number] - available_inventory[model_number]
            units_to_cancel[model_number] = discrepancy

    # print('\n')
    # pprint.pprint("Units to Cancel")
    # pprint.pprint(units_to_cancel)

    return units_to_cancel



def convert_xlsx_to_xls(filename, processing_dir, upload_directory):
    processed_file_path = os.path.join(processing_dir, filename)
    processing_workbook = load_workbook(processed_file_path)
    reference_sheet = processing_workbook.active
    
    completed_workbook = xlwt.Workbook()
    new_sheet = completed_workbook.add_sheet('Line Items')

    for row_idx, row in enumerate(reference_sheet.iter_rows()):
        for col_idx, cell in enumerate(row):
            if cell.is_date:
                date_value = cell.value
                date_string = date_value.strftime("%d-%b-%Y")
                new_sheet.write(row_idx, col_idx, date_string)
            else:
                new_sheet.write(row_idx, col_idx, cell.value)
    
    completed_filename = filename.replace('Processing.xlsx', 'Complete.xls')
    completed_file_path = os.path.join(upload_directory, completed_filename)
    completed_workbook.save(completed_file_path)
    os.remove(processed_file_path)
    return completed_workbook


def cancel_out_of_stock_units():
    print('hi')