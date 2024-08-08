# step_2_scripts.py

import pprint
import os
from openpyxl import load_workbook
from openpyxl.workbook import Workbook
from openpyxl.utils.datetime import from_excel
import xlwt


def calculate_units_to_cancel(requested_inventory, available_inventory):
    print("calculate_units_to_cancel")
    units_to_cancel = {}
    for model_number in requested_inventory:
        if requested_inventory[model_number] > available_inventory[model_number]:
            discrepancy = requested_inventory[model_number] - available_inventory[model_number]
            units_to_cancel[model_number] = discrepancy    
    return units_to_cancel


def cancel_out_of_stock_units(units_to_cancel, processing_filenames, processing_dir, min_order_value_us, min_order_value_ca):
    print('cancel_out_of_stock_units')
    print("processing_filenames: ", processing_filenames)
    print('\n')
    pprint.pprint("BEFORE - Units to cancel")
    pprint.pprint(units_to_cancel)

    new_workbook = Workbook()
    new_sheet = new_workbook.active
    new_sheet.title = 'Combined Data'
    order_value_dict = {}
    current_row = 1
    
    # Create new temporary sheet with CA + USD data
    for filename in processing_filenames.values():
        processed_file_path = os.path.join(processing_dir, filename)
        processing_workbook = load_workbook(processed_file_path)
        reference_sheet = processing_workbook.active
        current_row = copy_data_to_new_sheet(reference_sheet, new_sheet, current_row)
    
    # Get order values
    order_value_dict = create_order_value_dict(new_sheet, order_value_dict)
    pprint.pprint("BEFORE - Order Value Dict")
    pprint.pprint(order_value_dict)

    # First Pass: remove OOS units without putting orders below threshold (+ update order_value_dict)
    units_to_cancel, order_value_dict = remove_oos_units_above_threshold(new_sheet, units_to_cancel, order_value_dict, min_order_value_us, min_order_value_ca)
    
    print('\n')
    pprint.pprint("AFTER - Units to cancel")
    pprint.pprint(units_to_cancel)
    pprint.pprint("AFTER - Order Value Dict")
    pprint.pprint(order_value_dict)
    # If more units need to be cancelled
    if units_to_cancel: 
        print('HIIIII')
        # sort order value dict low to high

        # sort new sheet low to high

        # Second Pass: iterate through temp sheet and remove remianing OOS units

    # Create a new dict with order data from the new_sheet (order number, model number, units confirmed)

    # Update original sheet(s) with updated quantities + availability status

    # delete the combined-order-processing sheet

    # Update the global inventory_dict (for the copy function)


    order_value_dict = create_order_value_dict(new_sheet, order_value_dict)
    sorted_order_value_list = sorted(order_value_dict.items(), key=lambda item: item[1])
    
    # sort_sheet_by_order_value(new_sheet, sorted_order_value_list)
    
    new_file_path = os.path.join(processing_dir, 'Combined-Orders-Processing.xlsx')
    new_workbook.save(new_file_path)



def copy_data_to_new_sheet(reference_sheet, new_sheet, start_row):
    print('copy_data_to_new_sheet')
    for row in range(4, reference_sheet.max_row + 1):
        if not reference_sheet[f'A{row}'].value:
            break
        for col in range(1, reference_sheet.max_column + 1):
            new_sheet.cell(row=start_row, column=col, value=reference_sheet.cell(row=row, column=col).value)
        start_row += 1
    return start_row


def create_order_value_dict(sheet, order_value_dict):
    print('create_order_value_dict')
    for row in range(4, sheet.max_row + 1):
        order_number = sheet[f'A{row}'].value
        list_price = sheet[f'G{row}'].value
        confirmed_qty = sheet[f'L{row}'].value
        cost = list_price * confirmed_qty
        if order_number in order_value_dict.keys():
            order_value_dict[order_number] = order_value_dict[order_number] + cost
        else:
            order_value_dict[order_number] = cost
    return order_value_dict


def remove_oos_units_above_threshold(sheet, units_to_cancel, order_value_dict, min_order_value_us, min_order_value_ca):
    print('remove_oos_units_above_threshold')
    min_order_value_us = float(min_order_value_us.get())
    min_order_value_ca = float(min_order_value_ca.get())
    for row in range(1, sheet.max_row + 1):
        if not units_to_cancel:
            break
        print('\n')
        model_number = sheet[f'C{row}'].value
        print("Model Number: ", model_number)
        if model_number in units_to_cancel.keys():
            print("Entered -> ", model_number, "in units_to_cancel")
            cancel_amount = units_to_cancel[model_number]
            print("Cancel Amount: ", cancel_amount)
            order_number = sheet[f'A{row}'].value
            print("Order No.: ", order_number)
            price = sheet[f'I{row}'].value
            print("Price: ", price)
            confirmed_qty = sheet[f'L{row}'].value
            print("Confirmed Qty (before): ", confirmed_qty)
            currency = sheet[f'AF{row}'].value
            print("Currency: ", currency)
            if currency == "USD":
                min_val = min_order_value_us
                print("Confirming -> currency is USD")
            else:
                min_val = min_order_value_ca
                print("Confirming -> currency is CAD")
            while confirmed_qty > 0 and cancel_amount > 0:
                print("Entering while loop...")
                if (order_value_dict[order_number] - price) > min_val:
                    print("Removing 1 ", model_number, "from order", order_number)
                    # confirmed_quantity: remove 1
                    sheet[f'L{row}'].value = sheet[f'L{row}'].value - 1
                    # update units_to_cancel
                    units_to_cancel[model_number] = units_to_cancel[model_number] - 1
                    # update order_value_dict
                    order_value_dict[order_number] = order_value_dict[order_number] - price
                    # update counters
                    confirmed_qty = confirmed_qty - 1
                    cancel_amount = cancel_amount - 1
                    print("New confirmed quantity of ", model_number, ":", confirmed_qty)
                    print("New to cancel amount for ", model_number, ":", cancel_amount)
            print('\n')
            if units_to_cancel[model_number] == 0:
                print('No more units to cancel, yay')
                print("Old units to cancel dict: ", units_to_cancel)
                del units_to_cancel[model_number]
                print("Updated units to cancel dict: ", units_to_cancel)
            print('\n')
    return units_to_cancel, order_value_dict
            
                    


    




###############################




def sort_sheet_by_order_value(sheet, sorted_order_value_list):
    print('sort_sheet_by_order_value')
    pprint.pprint("Sorted Order Value List")
    pprint.pprint(sorted_order_value_list)
    





def convert_xlsx_to_xls(filename, processing_dir, upload_directory):
    print("convert_xlsx_to_xls")
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


