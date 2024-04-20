# file_processor.py

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import openpyxl
from openpyxl.workbook import Workbook
import xlrd
import subprocess
import os

def browse_files():
    file_path.set(filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")]))


def convert_xls_to_xlsx(src_file_path, dst_file_path):
    book_xls = xlrd.open_workbook(src_file_path)  
    book_xlsx = Workbook()  
    sheet_xls = book_xls.sheet_by_name('Line Items') 
    sheet_xlsx = book_xlsx.active 
    sheet_xlsx.title = 'Line Items'  
    for row in range(sheet_xls.nrows):
        for col in range(sheet_xls.ncols):
            sheet_xlsx.cell(row=row + 1, column=col + 1).value = sheet_xls.cell_value(row, col)
    book_xlsx.save(dst_file_path)


def process_file():
    if not file_path.get():
        messagebox.showerror("Error", "Please select a file first!")
        return

    try:
        original_file_path = file_path.get()
        base_folder = os.path.dirname(original_file_path)
        new_path = os.path.join(base_folder, 'temp.xlsx')

        if file_path.get().endswith('.xls'):
            convert_xls_to_xlsx(file_path.get(), new_path)
            file_path.set(new_path)

        workbook = openpyxl.load_workbook(file_path.get())
        if 'Line Items' in workbook.sheetnames:
            sheet = workbook['Line Items']
            if sheet['A3'].value == 'Order/PO Number':
                python_exec_path = os.path.join(project_root_dir, 'venv', 'Scripts', 'python.exe')
                subprocess.run([python_exec_path, 'calculate_inventory.py', file_path.get()], check=True)
                messagebox.showinfo("Success", "File has been processed and saved successfully.")
            else:
                messagebox.showerror("Error", "The cell A3 in 'Line Items' does not contain 'Order/PO Number'.")
        else:
            messagebox.showerror("Error", "The 'Line Items' sheet does not exist in the workbook.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process the file: {str(e)}")


# Create the main window
root = tk.Tk()
root.title("Excel File Processor")

# Layout configuration
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

# Variables
file_path = tk.StringVar()

# Widgets
frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

label = ttk.Label(frame, text="Select an Excel File:")
label.grid(column=0, row=0, sticky=tk.W, pady=(0, 10))

file_entry = ttk.Entry(frame, textvariable=file_path, width=50)
file_entry.grid(column=1, row=0, sticky=(tk.W, tk.E))

browse_button = ttk.Button(frame, text="Browse", command=browse_files)
browse_button.grid(column=2, row=0, sticky=tk.W)

process_button = ttk.Button(frame, text="Process File", command=process_file)
process_button.grid(column=1, row=1, pady=(10, 0))

# Start the GUI
root.mainloop()
