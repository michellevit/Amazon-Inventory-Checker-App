# step_2_scripts.py

import os
import shutil


def review_inventory(requested_inventory, available_inventory):
    print('hi')

    # if requested_inventory == available_inventory: 
    #     print('Do nothing!')
    #     directory, filename = os.path.split(original_path)
    #     name, extension = os.path.splitext(filename)
    #     new_name = name + ' - complete' + extension
    #     new_path = os.path.join(directory, new_name)
    #     shutil.copyfile(original_path, new_path)
    # else:
    #     print("UHOH")
    # confirmation_message = (f"File has been processed\n\nThe completed file will be in the same folder as the original Amazon vendor download file, and it will be named: \n\n '{new_name}'\n\nSubmit this NEW file to Amazon to confirm the {country} orders.")
    # return confirmation_message


    # use xldr to read the file at original_path
    # create a dictionary called po_value + organize it from lowest val to highest val
    # if requested_inventory != available_inventory:
    # # create a new dict called items_to_cancel (this will be requested item - available item)
    # # create a new dict called item_value (key: model_number, value cost)
    # # Go through each line in the spreadsheet:
    # # # Get the PO number
    # # # Get the PO value
    # # # While the item is in the items_to_cancel dict and the po_value > min_value_threshold
    # # # # remove 1 from the quantity_confirmed column
    # # # # remove 1 from the items_to_cancel
    # # # # if the item in items_to_cancel is 0 then remove it from the dict
    # # # # remove the item_cost from the po_value dict
    # # Once all the rows have been iterated, if there are still items in the items_to_cancel then:
    # # Iterate through the po_value dictionary (sorted low to high):
    # # # Iterate through the rows
    # # # # if Order/PO number matches and model_number is in the items_to_cancel dict:
    # # # # # while item is in the items_to_cancel dict and quantity_confirmed > 0:
    # # # # # # remove 1 from the quantity_confirmed and remove 1 from the items_to_cancel
    # # # # # # if the items_to_cancel item value = 0 then remove it from the dict
    # # Iterate through each row in the sheet
    # # # If the 'Quantity Confirmed' value is 0 then change that row's availability status to 'OS - Cancelled: Out of stock'
    # print("\n Available Inventory:")
    # print("-" * 40)
    # print("{:<15} | {:>10}".format("Model Number", "Quantity"))
    # print("-" * 40)
    # for model, quantity in available_inventory.items():
    #     print("{:<15} | {:>10}".format(model, quantity))
    # print("-" * 40)


def convert_xlsx_to_xls(src_file_path, dst_file_path):
    print('hi')

