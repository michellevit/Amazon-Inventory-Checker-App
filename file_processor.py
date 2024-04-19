import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import openpyxl

def browse_files():
    file_path.set(filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")]))
    if file_path.get():
        messagebox.showinfo("File Selected", f"You have selected {file_path.get()}")

def process_file():
    if not file_path.get():
        messagebox.showerror("Error", "Please select a file first!")
        return
    
    try:
        # Load the workbook
        workbook = openpyxl.load_workbook(file_path.get())
        sheet = workbook.active

        # Example manipulation: Read and print all values
        for row in sheet.iter_rows(values_only=True):
            print(row)  # Placeholder for actual data manipulation

        # Save the workbook (optional: save as new file)
        workbook.save(file_path.get())
        messagebox.showinfo("Success", "File has been processed and saved successfully.")

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
