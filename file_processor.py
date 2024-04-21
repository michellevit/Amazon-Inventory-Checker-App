# file_processor.py

import json
import openpyxl
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from scripts.step_1_scripts import convert_xls_to_xlsx, check_file_valid, calculate_inventory, copy_to_clipboard
from scripts.step_2_scripts import review_inventory, convert_xlsx_to_xls


def load_min_order_value():
    try:
        with open('min_order_value.json', 'r') as file:
            data = json.load(file)
            return data['min_order_value']
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        print("Error with min_order_value")
        return 380


def save_min_order_value(value):
    with open('min_order_value.json', 'w') as file:
        json.dump({'min_order_value': value}, file)


def browse_files():
    file_path.set(filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")]))
    clear_frame(inventory_frame)  


def process_file():
    if not file_path.get():
        messagebox.showerror("Error", "Please select a file first!")
        return
    try:
        original_path = file_path.get()
        temp_path = None
        if original_path.endswith('.xls'):
            workbook = convert_xls_to_xlsx(original_path)
        elif original_path.endswith('.xlsx'):
            directory, original_filename = os.path.split(original_path)
            filename_without_extension, _ = os.path.splitext(original_filename)
            new_filename = f"{filename_without_extension} - temp.xlsx"
            temp_path = os.path.join(directory, new_filename)
            os.rename(original_path, temp_path)
            workbook = openpyxl.load_workbook(temp_path)
        if check_file_valid(workbook):
            requested_inventory, currency = calculate_inventory(workbook)
            display_inventory_form(requested_inventory, currency, original_path)
            toggle_order_value_edit(False)
            if temp_path:
                os.remove(temp_path)
                os.rename(temp_path, original_path)
        else:
            messagebox.showerror("Error", "The file is not supported by this program.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process the file: {str(e)}")
        if temp_path and os.path.exists(temp_path):
            os.rename(temp_path, original_path)


def change_order_value():
    try:
        value = int(temp_order_value.get())
        if not (0 < value < 10000):
            raise ValueError("Value must be between 1 and 9999.")
        save_min_order_value(value)
        min_order_value.set(str(value))
        order_value_label.config(text=f"Minimum Order Value: ${min_order_value.get()}")
        messagebox.showinfo("Success", "Minimum order value updated.")
        temp_order_value.set('') 
    except ValueError as e:
        messagebox.showerror("Error", "Invalid input. Please enter a whole number between 1 and 9999.")


def display_inventory_form(requested_inventory, currency, original_path):
    clear_frame(inventory_frame)  
    bold_font = ('Helvetica', 9, 'bold')
    ttk.Label(inventory_frame, text="Model Number", font=bold_font, anchor="center").grid(row=0, column=0, sticky='ew', padx=5, pady=5)
    ttk.Label(inventory_frame, text="Requested", font=bold_font, anchor="center").grid(row=0, column=1, sticky='ew', padx=5, pady=5)
    ttk.Label(inventory_frame, text="Available", font=bold_font, anchor="center").grid(row=0, column=2, sticky='ew', padx=5, pady=5)
    for idx, (model, quantity) in enumerate(requested_inventory.items(), start=1):
        ttk.Label(inventory_frame, text=model).grid(row=idx, column=0)
        ttk.Label(inventory_frame, text=str(quantity)).grid(row=idx, column=1)
        entry = ttk.Entry(inventory_frame, width=10, justify=tk.CENTER)
        entry.insert(0, str(quantity))
        entry.grid(row=idx, column=2)
        entries[model] = entry
    # Buttons Frame
    button_frame = ttk.Frame(inventory_frame)
    button_frame.grid(row=len(requested_inventory) + 1, column=0, columnspan=3, pady=15) 
    copy_button = ttk.Button(button_frame, text="Copy", command=lambda: copy_to_clipboard(currency, requested_inventory))
    copy_button.pack(side=tk.LEFT, padx=5)
    submit_button = ttk.Button(button_frame, text="Submit", command=lambda: submit_inventory(entries, requested_inventory, original_path, currency))
    submit_button.pack(side=tk.LEFT, padx=5)  


def submit_inventory(entries, requested_inventory, original_path, currency):
    available_inventory = {model: int(entry.get()) for model, entry in entries.items()}
    confirmation_message = review_inventory(requested_inventory, available_inventory, original_path, min_order_value, currency)
    messagebox.showinfo("Notice", confirmation_message)
    toggle_order_value_edit(True)
    file_path.set('')
    clear_frame(inventory_frame)
    inventory_frame.pack_forget()


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def toggle_order_value_edit(show):
    if show:
        temp_order_value.set('')
        order_value_entry.pack(side=tk.LEFT, padx=5)
        change_button.pack(side=tk.LEFT, padx=5)
    else:
        order_value_entry.pack_forget()
        change_button.pack_forget()
    order_value_label.config(text=f"Minimum Order Value: ${min_order_value.get()}")



def setup_gui():
    root = tk.Tk()
    root.title("Amazon Confirmation Processor")
    root.geometry('500x600')
    
    global file_path, file_entry, min_order_value, temp_order_value, order_value_label, order_value_entry, change_button, order_value_frame, inventory_frame, entries, canvas
    file_path = tk.StringVar()
    min_order_value = tk.StringVar(value=str(load_min_order_value())) 
    temp_order_value = tk.StringVar()
    entries = {}

    # Main Frame
    main_frame = ttk.Frame(root, padding=10)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Minimum Order Value Frame
    order_value_container = ttk.Frame(main_frame)
    order_value_container.pack(fill=tk.X, pady=10)
    order_value_frame = ttk.Frame(order_value_container, padding=10)
    order_value_frame.pack()
    order_value_label = ttk.Label(order_value_frame, text=f"Minimum Order Value: ${min_order_value.get()}")
    order_value_label.pack(side=tk.LEFT, padx=(0, 15))
    order_value_entry = ttk.Entry(order_value_frame, textvariable=temp_order_value, width=4)
    order_value_entry.pack(side=tk.LEFT)
    change_button = ttk.Button(order_value_frame, text="Change", command=change_order_value)
    change_button.pack(side=tk.LEFT, padx=(10, 0))
    toggle_order_value_edit(True)

    # File Input Frame
    file_input_frame = ttk.Frame(main_frame, padding=10)
    file_input_frame.pack(fill=tk.X, pady=10)
    file_input_container = ttk.Frame(file_input_frame)
    file_input_container.pack(pady=5)
    select_file_label = ttk.Label(file_input_container, text="Select File:")
    select_file_label.pack(side=tk.LEFT, padx=5, pady=5)
    file_entry = ttk.Entry(file_input_container, textvariable=file_path, state='readonly', width=50, style='White.TEntry')
    file_entry.pack(side=tk.LEFT, padx=5, pady=5)
    browse_button = ttk.Button(file_input_container, text="Browse", command=browse_files)
    browse_button.pack(side=tk.LEFT, padx=5, pady=5)
    file_input_container.pack_configure(expand=True)
    file_input_container.pack_configure(side=tk.TOP)
    process_button = ttk.Button(file_input_frame, text="Process", command=process_file)
    process_button.pack(pady=10)

    # Separator for visual distinction
    ttk.Separator(main_frame).pack(fill=tk.X, pady=5)

    # Setup for scrolling and dynamic centering
    scroll_frame = ttk.Frame(main_frame)
    scroll_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    canvas = tk.Canvas(scroll_frame, highlightthickness=0)
    scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    inventory_frame = ttk.Frame(canvas)
    inventory_width = 450

    # Inventory Frame 
    inventory_x_position = (canvas.winfo_reqwidth() - inventory_width) // 2
    window = canvas.create_window((inventory_x_position, 0), window=inventory_frame, anchor='n', width=inventory_width)
    canvas.configure(yscrollcommand=scrollbar.set)
    inventory_frame.grid_columnconfigure(0, weight=1, minsize=150)
    inventory_frame.grid_columnconfigure(1, weight=1, minsize=150)
    inventory_frame.grid_columnconfigure(2, weight=1, minsize=150)
    def onCanvasConfigure(event):
        """Adjust the window's position to stay centered."""
        nonlocal window
        inventory_x_position = (event.width - inventory_width) // 2
        canvas.coords(window, (inventory_x_position, 0))
    canvas.bind("<Configure>", onCanvasConfigure)
    def onFrameConfigure(canvas):
        """Update the scroll region to encompass the inner frame."""
        canvas.configure(scrollregion=canvas.bbox("all"))
    inventory_frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

    root.mainloop()


if __name__ == "__main__":
    setup_gui()