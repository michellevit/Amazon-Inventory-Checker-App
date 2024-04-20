# calculate_inventory.py

import sys
import openpyxl
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_workbook(file_path):
    print('hi')
    try:
        workbook = openpyxl.load_workbook(file_path)
        if 'Line Items' in workbook.sheetnames:
            sheet = workbook['Line Items']  # Accessing specific sheet directly
        else:
            logging.error("The 'Line Items' sheet does not exist in the workbook.")
            return
        
        logging.info("Processing rows in the workbook...")
        for row in sheet.iter_rows(values_only=True):
            print(row)  # This will print each row's data to the console
        workbook.save(file_path)
        logging.info("Workbook processed and saved successfully.")
    except Exception as e:
        logging.error(f"Failed to process the workbook: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        logging.error("Usage: python calculate_inventory.py <path_to_excel_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    logging.info(f"Processing file: {file_path}")
    process_workbook(file_path)
