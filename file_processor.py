# file_processor.py

import json
import openpyxl
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from scripts.step_1_scripts import convert_xls_to_xlsx, check_file_valid, calculate_inventory, find_vendor_origins, copy_to_clipboard
from scripts.step_2_scripts import review_inventory, convert_xlsx_to_xls


def load_min_order_value(currency):
    try:
        with open('min_order_value.json', 'r') as file:
            data = json.load(file)
            if currency == 'us':
                return data['min_order_value_us']
            else:
                return data['min_order_value_ca']
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        print("Error with min_order_value")
        return 380


def save_min_order_value(currency, value):
    try:
        with open('min_order_value.json', 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    if currency == 'us':
        data['min_order_value_us'] = value
    else:
        data['min_order_value_ca'] = value
    with open('min_order_value.json', 'w') as file:
        json.dump(data, file)


def browse_files(currency):
    if currency == "us":
        file_path_us.set(filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")]))
    else:
        file_path_ca.set(filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")]))
    clear_frame(inventory_frame)  


def process_files():
    if not file_path_ca.get() and not file_path_us.get():
        messagebox.showerror("Error", "Please select at least one file first.")
        return
    requested_inventory = {}
    submitted_files = {}
    if file_path_us.get():
        requested_inventory = process_file(file_path_us.get(), 'us', requested_inventory)
        submitted_files['us'] = True
    if file_path_ca.get():
        requested_inventory = process_file(file_path_ca.get(), 'ca', requested_inventory)
        submitted_files['ca'] = True
    vendor_origins = find_vendor_origins(submitted_files)    
    toggle_order_value_edit('na', False)
    display_inventory_form(requested_inventory, vendor_origins)


def process_file(file_path, currency, requested_inventory):
    try:
        original_path = file_path
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
        if check_file_valid(workbook, currency):
            requested_inventory = calculate_inventory(workbook, requested_inventory)
            if temp_path:
                os.remove(temp_path)
                os.rename(temp_path, original_path)
            return requested_inventory
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process the file: {str(e)}")
        if temp_path and os.path.exists(temp_path):
            os.rename(temp_path, original_path)
        raise 


def change_order_value(currency):
    try:
        if currency == 'us':
            temp_value = temp_order_value_us.get()
            min_order_value_var = min_order_value_us
            order_value_label_var = order_value_label_us
        else:
            temp_value = temp_order_value_ca.get()
            min_order_value_var = min_order_value_ca
            order_value_label_var = order_value_label_ca

        value = int(temp_value)
        if not (0 < value < 10000):
            raise ValueError("Value must be between 1 and 9999.")
        save_min_order_value(currency, value)
        min_order_value_var.set(str(value))
        order_value_label_var.config(text=f"Minimum Order Value: {currency.upper()}D ${value}")
        if currency == 'us':
            temp_order_value_us.set('')
        else:
            temp_order_value_ca.set('')
        messagebox.showinfo("Success", f"Minimum order value for {currency.upper()} updated.")
    except ValueError as e:
        messagebox.showerror("Error", "Invalid input. Please enter a whole number between 1 and 9999.")


def display_inventory_form(requested_inventory, vendor_origins):
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
    clear_button = ttk.Button(button_frame, text="Clear", command=reset)
    clear_button.pack(side=tk.LEFT, padx=5)  
    copy_button = ttk.Button(button_frame, text="Copy", command=lambda: copy_to_clipboard(requested_inventory, vendor_origins))
    copy_button.pack(side=tk.LEFT, padx=5)
    submit_button = ttk.Button(button_frame, text="Submit", command=lambda: submit_inventory(entries, requested_inventory))
    submit_button.pack(side=tk.LEFT, padx=5)


def submit_inventory(entries, requested_inventory):
    available_inventory = {model: int(entry.get()) for model, entry in entries.items()}
    confirmation_message = review_inventory(requested_inventory, available_inventory)
    messagebox.showinfo("Notice", confirmation_message)
    toggle_order_value_edit('us', True)
    toggle_order_value_edit('ca', True)
    file_path_us.set('')
    file_path_ca.set('')
    clear_frame(inventory_frame)
    inventory_frame.pack_forget()


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def reset():
    toggle_order_value_edit('us', True)
    toggle_order_value_edit('ca', True)
    file_path_us.set('')
    file_path_ca.set('')
    clear_frame(inventory_frame)
    inventory_frame.pack_forget()   


def toggle_order_value_edit(currency, show):
    if show:
        if currency == "us":
            temp_order_value_us.set('')
            order_value_entry_us.pack(side=tk.LEFT, padx=5)
            change_button_us.pack(side=tk.LEFT, padx=5)
        else:
            temp_order_value_ca.set('')
            order_value_entry_ca.pack(side=tk.LEFT, padx=5)
            change_button_ca.pack(side=tk.LEFT, padx=5)
    else:
        order_value_entry_us.pack_forget()
        order_value_entry_ca.pack_forget()
        change_button_us.pack_forget()
        change_button_ca.pack_forget()



def setup_gui():
    root = tk.Tk()
    root.title("Amazon Confirmation Processor")
    root.geometry('850x600')

    global file_path_us, file_entry_us, min_order_value_us, temp_order_value_us
    global file_path_ca, file_entry_ca, min_order_value_ca, temp_order_value_ca
    global order_value_label_us, order_value_entry_us, change_button_us
    global order_value_label_ca, order_value_entry_ca, change_button_ca
    global inventory_frame, entries, canvas

    # Variables for US file input
    file_path_us = tk.StringVar()
    min_order_value_us = tk.StringVar(value=str(load_min_order_value('us')))
    temp_order_value_us = tk.StringVar()

    # Variables for CA file input
    file_path_ca = tk.StringVar()
    min_order_value_ca = tk.StringVar(value=str(load_min_order_value('ca')))
    temp_order_value_ca = tk.StringVar()

    entries = {}

    # Main Frame
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=10)

    # US Container Frame
    us_container_frame = ttk.Frame(main_frame)
    us_container_frame.pack(pady=10)


    # US File Input Frame
    file_input_frame_us = ttk.Frame(us_container_frame, padding=5)
    file_input_frame_us.pack(side=tk.LEFT, padx=5)
    select_file_label_us = ttk.Label(file_input_frame_us, text="Amazon US File:")
    select_file_label_us.pack(side=tk.LEFT, padx=5, pady=5)
    file_entry_us = ttk.Entry(file_input_frame_us, textvariable=file_path_us, state='readonly', width=50, style='White.TEntry')
    file_entry_us.pack(side=tk.LEFT, padx=5, pady=5)
    browse_button_us = ttk.Button(file_input_frame_us, text="Browse", command=lambda: browse_files('us'))
    browse_button_us.pack(side=tk.LEFT, padx=5, pady=5)

    # US Minimum Order Value Frame
    order_value_frame_us = ttk.Frame(us_container_frame, padding=5)
    order_value_frame_us.pack(side=tk.RIGHT, padx=5)
    order_value_label_us = ttk.Label(order_value_frame_us, text=f"Minimum Order Value: USD ${min_order_value_us.get()}")
    order_value_label_us.pack(side=tk.LEFT)
    order_value_entry_us = ttk.Entry(order_value_frame_us, textvariable=temp_order_value_us, width=4)
    order_value_entry_us.pack(side=tk.LEFT)
    change_button_us = ttk.Button(order_value_frame_us, text="Change", command=lambda: change_order_value('us'))
    change_button_us.pack(side=tk.LEFT)
    toggle_order_value_edit('us', True)

    # CA Container Frame
    ca_container_frame = ttk.Frame(main_frame)
    ca_container_frame.pack(pady=5)

    # CA File Input Frame
    file_input_frame_ca = ttk.Frame(ca_container_frame, padding=5)
    file_input_frame_ca.pack(side=tk.LEFT, padx=5)
    select_file_label_ca = ttk.Label(file_input_frame_ca, text="Amazon CA File:")
    select_file_label_ca.pack(side=tk.LEFT, padx=5, pady=5)
    file_entry_ca = ttk.Entry(file_input_frame_ca, textvariable=file_path_ca, state='readonly', width=50, style='White.TEntry')
    file_entry_ca.pack(side=tk.LEFT, padx=5, pady=5)
    browse_button_ca = ttk.Button(file_input_frame_ca, text="Browse", command=lambda: browse_files('ca'))
    browse_button_ca.pack(side=tk.LEFT, padx=5, pady=5)

    # CA Minimum Order Value Frame
    order_value_frame_ca = ttk.Frame(ca_container_frame, padding=5)
    order_value_frame_ca.pack(side=tk.RIGHT, padx=5)
    order_value_label_ca = ttk.Label(order_value_frame_ca, text=f"Minimum Order Value: CAD ${min_order_value_ca.get()}")
    order_value_label_ca.pack(side=tk.LEFT)
    order_value_entry_ca = ttk.Entry(order_value_frame_ca, textvariable=temp_order_value_ca, width=4)
    order_value_entry_ca.pack(side=tk.LEFT)
    change_button_ca = ttk.Button(order_value_frame_ca, text="Change", command=lambda: change_order_value('ca'))
    change_button_ca.pack(side=tk.LEFT)
    toggle_order_value_edit('ca', True)

    # Process Button
    process_button = ttk.Button(main_frame, text="Process", command=process_files)
    process_button.pack(pady=10)

    # Separator for visual distinction
    ttk.Separator(main_frame).pack(fill=tk.X, pady=5)

     # Setup for scrolling
    scroll_frame = ttk.Frame(main_frame)
    scroll_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    canvas = tk.Canvas(scroll_frame, width=root.winfo_screenwidth(), highlightthickness=0)
    scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    inventory_frame = ttk.Frame(canvas)
    inventory_width = 400

    # Inventory Frame
    window_width = root.winfo_reqwidth()
    inventory_x_position = (window_width - inventory_width) // 2
    window = canvas.create_window((inventory_x_position, 0), window=inventory_frame, anchor='n', width=inventory_width)
    canvas.configure(yscrollcommand=scrollbar.set)
    inventory_frame.grid_columnconfigure(0, weight=1, minsize=150)
    inventory_frame.grid_columnconfigure(1, weight=1, minsize=150)
    inventory_frame.grid_columnconfigure(2, weight=1, minsize=150)

    def onCanvasConfigure(event):
        nonlocal window, inventory_width
        root.update_idletasks()
        window_width = event.width
        inventory_width = 400
        inventory_x_position = (window_width - inventory_width) // 2
        canvas.itemconfig(window, width=inventory_width)
        canvas.coords(window, (inventory_x_position, 0))

    canvas.bind("<Configure>", onCanvasConfigure)

    def onFrameConfigure(canvas):
        """Update the scroll region to encompass the inner frame."""
        canvas.configure(scrollregion=canvas.bbox("all"))

    inventory_frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
    root.mainloop()


if __name__ == "__main__":
    setup_gui()