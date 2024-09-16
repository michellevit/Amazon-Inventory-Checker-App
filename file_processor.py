# file_processor.py

import json
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from scripts.step_1_scripts import *
from scripts.step_2_scripts import *
import shutil


# Set the working directory to the location of the executable
if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))
else:
    os.chdir(os.path.dirname(__file__))


def load_min_order_value(currency):
    try:
        file_path = os.path.join('min_order_value.json')
        with open(file_path, 'r') as file:
            data = json.load(file)
            if currency == 'us':
                return data.get('min_order_value_us', 380)
            else:
                return data.get('min_order_value_ca', 380)
    except FileNotFoundError:
        print("Error: 'min_order_value.json' file not found. Using default value 380.")
    except KeyError as e:
        print(f"Error: Key {e} not found in the JSON data. Using default value 380.")
    except json.JSONDecodeError:
        print("Error: JSON decode error occurred. Using default value 380.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}. Using default value 380.")
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
    if currency == 'us':
        min_order_value_us.set(str(load_min_order_value('us')))
    else:
        min_order_value_ca.set(str(load_min_order_value('ca')))


def browse_files(currency):
    if currency == "us":
        file_path_us.set(filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")]))
    else:
        file_path_ca.set(filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")]))
    clear_frame(inventory_frame)


def process_files():
    processing_filenames = {}
    if not file_path_ca.get() and not file_path_us.get():
        messagebox.showerror("Error", "Please select at least one file first.")
        return
    processing_dir = os.path.join(os.getcwd(), 'processing')
    os.makedirs(processing_dir, exist_ok=True)
    clear_processing_directory(processing_dir)
    requested_inventory = {}
    submitted_files = {}
    po_value_dict = {}
    orders_to_cancel_array = []
    processing_filenames = {}
    if file_path_us.get():
        requested_inventory, filename_processing, po_value_dict, orders_to_cancel_array = process_file(file_path_us.get(), 'us', requested_inventory, po_value_dict, orders_to_cancel_array, processing_dir)
        submitted_files['us'] = True
        upload_directory = os.path.dirname(file_path_us.get())
        processing_filenames['us'] = filename_processing
    if file_path_ca.get():
        requested_inventory, filename_processing, po_value_dict, orders_to_cancel_array = process_file(file_path_ca.get(), 'ca', requested_inventory, po_value_dict, orders_to_cancel_array, processing_dir)
        submitted_files['ca'] = True
        upload_directory = os.path.dirname(file_path_ca.get())
        processing_filenames['ca'] = filename_processing
    update_browse_button('process')
    remove_old_completed_files(upload_directory)
    vendor_origins = find_vendor_origins(submitted_files)
    hide_order_value_edit_section(True)
    check_if_orders_over_min(requested_inventory, vendor_origins, processing_filenames, processing_dir, upload_directory)


def clear_processing_directory(processing_dir):
    if not os.listdir(processing_dir):
        return
    for filename in os.listdir(processing_dir):
        file_path = os.path.join(processing_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')


def process_file(file_path, currency, requested_inventory, po_value_dict, orders_to_cancel_array, processing_dir):
    clear_frame(message_frame)
    try:
        original_path = file_path
        if original_path.endswith('.xls'):
            workbook, filename_processing, new_file_path = convert_xls_to_xlsx(original_path, currency, processing_dir)
        else:
            workbook, filename_processing, new_file_path = create_new_file(original_path, currency, processing_dir)
        if check_file_valid(workbook, currency):
            if currency == 'us':
                min_order_value = min_order_value_us.get()
            else:
                min_order_value = min_order_value_ca.get()
            workbook, orders_to_cancel_array = cancel_orders_below_min(workbook, min_order_value, new_file_path, po_value_dict, orders_to_cancel_array)
            workbook = update_hand_off_date(workbook, new_file_path)
            requested_inventory = calculate_inventory(workbook, requested_inventory, orders_to_cancel_array)
            return requested_inventory, filename_processing, po_value_dict, orders_to_cancel_array
        else:
            capitalized_currency = currency.upper()
            messagebox.showerror("Error", f"Failed to process the file.\n\nNote: Please ensure that the {capitalized_currency} file has line items requests.")
            if currency == 'us':
                file_path_us.set('')
            else:
                file_path_ca.set('')
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process the file.\n\nERROR: {str(e)}\n")
        raise 


def remove_old_completed_files(upload_directory):
    # Remove any previous 'Complete' reports from directory
    old_filenames = ["Amazon-Orders-US-Complete.xls", "Amazon-Orders-CA-Complete.xls"]
    for old_filename in old_filenames:
        old_file_path = os.path.join(upload_directory, old_filename)
        old_file_path = os.path.normpath(old_file_path)
        if os.path.exists(old_file_path):
            try:
                os.remove(old_file_path)
            except Exception as e:
                messagebox.showerror("Error", f"Error removing file {old_file_path}: {e}\n\nERROR: {str(e)}\n")
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


def check_if_orders_over_min(requested_inventory, vendor_origins, processing_filenames, processing_dir, upload_directory):
    # If no orders are over min_value threshold
    if all(value == 0.0 for value in requested_inventory.values()):
        prep_files_for_submission(processing_filenames, processing_dir, upload_directory, requested_inventory, vendor_origins, result="all below threshold")
    else:
        display_inventory_form(requested_inventory, vendor_origins, processing_filenames, processing_dir, upload_directory)


def display_inventory_form(requested_inventory, vendor_origins, processing_filenames, processing_dir, upload_directory):
    entries.clear()
    # Container frame for labels
    inventory_form_container = ttk.Frame(inventory_frame)
    inventory_form_container.grid(row=0, column=0, columnspan=3, pady=5)
    
    bold_font = ('Helvetica', 9, 'bold')        
    # Labels for Model Number, Requested, Available
    ttk.Label(inventory_form_container, text="Model Number", font=bold_font, anchor="center", width=20).grid(row=0, column=0, sticky='ew', padx=5, pady=5)
    ttk.Label(inventory_form_container, text="Requested", font=bold_font, anchor="center", width=20).grid(row=0, column=1, sticky='ew', padx=5, pady=5)
    ttk.Label(inventory_form_container, text="Available", font=bold_font, anchor="center", width=20).grid(row=0, column=2, sticky='ew', padx=5, pady=5)

    # Populate requested inventory data
    for idx, (model, quantity) in enumerate(requested_inventory.items(), start=1):
        ttk.Label(inventory_form_container, text=model, anchor="center", width=20, justify="center").grid(row=idx, column=0, sticky='ew')
        ttk.Label(inventory_form_container, text=str(quantity), width=20, anchor="center", justify="center").grid(row=idx, column=1)
        entry = ttk.Entry(inventory_form_container, width=10, justify=tk.CENTER)
        entry.insert(0, str(quantity))
        entry.grid(row=idx, column=2, padx=5, pady=2)
        entries[model] = entry
    
    # Buttons Frame
    button_frame = ttk.Frame(inventory_frame)
    button_frame.grid(row=1, column=0, columnspan=3, pady=10) 
    clear_button = ttk.Button(button_frame, text="Clear", command=reset)
    clear_button.pack(side=tk.LEFT, padx=5)  
    copy_button = ttk.Button(button_frame, text="Copy", command=lambda: copy_to_clipboard(requested_inventory, vendor_origins, False))
    copy_button.pack(side=tk.LEFT, padx=5)
    submit_button = ttk.Button(button_frame, text="Submit", command=lambda: submit_inventory(entries, requested_inventory, processing_filenames, processing_dir, upload_directory, vendor_origins))
    submit_button.pack(side=tk.LEFT, padx=5)
    
    # Pack the inventory frame back into the main frame
    inventory_frame.pack(fill=tk.BOTH, expand=True)


def submit_inventory(entries, requested_inventory, processing_filenames, processing_dir, upload_directory, vendor_origins):
    available_inventory = {}
    for model, entry in entries.items():
        try:
            available_qty = int(entry.get())
        except ValueError:
            messagebox.showerror("Error", f"Available quantity for {model} must be between 0 and the requested quantity ({requested_qty}).")
            return
        requested_qty = requested_inventory[model]
        if available_qty > requested_qty or available_qty < 0:
            messagebox.showerror("Error", f"Available quantity for {model} must be between 0 and the requested quantity ({requested_qty}).")
            return
        
        available_inventory[model] = available_qty
    try:
        units_to_cancel = calculate_units_to_cancel(requested_inventory, available_inventory)
        if units_to_cancel:
            accepted_inventory = cancel_out_of_stock_units(units_to_cancel, available_inventory, processing_filenames, processing_dir, min_order_value_us, min_order_value_ca)
        else:
            accepted_inventory = requested_inventory

        prep_files_for_submission(processing_filenames, processing_dir, upload_directory, accepted_inventory, vendor_origins)
    except PermissionError:
        messagebox.showerror("File Error", "The file is open. Please close the file before clicking submit.")
        return


def prep_files_for_submission(processing_filenames, processing_dir, upload_directory, accepted_inventory, vendor_origins, result="files ready"):
    if 'us' in processing_filenames:
        us_filename = processing_filenames['us']
        convert_xlsx_to_xls(us_filename, processing_dir, upload_directory)
    if 'ca' in processing_filenames: 
        ca_filename = processing_filenames['ca']
        convert_xlsx_to_xls(ca_filename, processing_dir, upload_directory)
    display_final_message(result, processing_filenames, processing_dir, upload_directory, accepted_inventory, vendor_origins)


def display_final_message(result, processing_filenames, processing_dir, upload_directory, accepted_inventory, vendor_origins):
    clear_frame(inventory_frame)
    clear_processing_directory(processing_dir)
    final_message_container = ttk.Frame(message_frame)
    final_message_container.grid(row=0, column=0, columnspan=3, pady=5)

    if accepted_inventory:
        # Create a frame for the Treeview with a scrollbar
        tree_frame = ttk.Frame(final_message_container)
        tree_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

        # Create a scrollbar
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Determine the number of rows in accepted_inventory and set a maximum display limit
        max_display_rows = 10
        num_rows = min(len(accepted_inventory), max_display_rows)

        # Create Treeview for confirmed inventory
        tree = ttk.Treeview(tree_frame, columns=("Model Number", "Confirmed Quantity"), show='headings', height=num_rows, yscrollcommand=tree_scroll.set)
        tree.heading("Model Number", text="Model Number")
        tree.heading("Confirmed Quantity", text="Confirmed Quantity")
        tree.column("Model Number", anchor="center", width=150)
        tree.column("Confirmed Quantity", anchor="center", width=150)

        # Configure the scrollbar
        tree_scroll.config(command=tree.yview)

        # Sort the accepted_inventory dictionary by model_number
        sorted_inventory = sorted(accepted_inventory.items())

        # Populate Treeview with sorted accepted inventory data
        for model_number, confirmed_qty in sorted_inventory:
            tree.insert('', 'end', values=(model_number, confirmed_qty))

        tree.pack(fill=tk.BOTH, expand=True)
        table_row = 1  # Set the row for the message below the table
    else:
        table_row = 0  # Set the row for the message at the top if no table

    # Message label
    if len(processing_filenames) == 2:
        file_plurality = "files"
    else:
        file_plurality = "file"
    filenames = []
    if processing_filenames.get('us'):
        us_filename = processing_filenames.get('us')
        completed_filename = us_filename.replace('Processing.xlsx', 'Complete.xls')
        filenames.append(completed_filename)
    if processing_filenames.get('ca'):
        ca_filename = processing_filenames.get('ca')
        completed_filename = ca_filename.replace('Processing.xlsx', 'Complete.xls')
        filenames.append(completed_filename)
    if result == "all below threshold":
        message = (
            f"All order requests were under the minimum threshold - please submit the following {file_plurality} to cancel all order requests:\n\n"
            + "\n".join(filenames)
            + f"\n\nDirectory: {upload_directory}"
        )
    elif not accepted_inventory:
        message = (
            f"No orders were accepted - please submit the following {file_plurality} to cancel all order requests:\n\n"
            + "\n".join(filenames)
            + f"\n\nDirectory: {upload_directory}"
        )
    elif result == "files ready":
        message = (
            f"File processing complete - please submit the following {file_plurality} to complete Amazon Order Confirmation Process:\n\n"
            + "\n".join(filenames)
            + f"\n\nDirectory: {upload_directory}"
        )
    ttk.Label(final_message_container, text=message, anchor="center", justify="center").grid(row=table_row, column=0, columnspan=3, pady=20)

    # Buttons Frame
    button_frame = ttk.Frame(message_frame)
    button_frame.grid(row=table_row + 1, column=0, columnspan=3, pady=10)
    if accepted_inventory:
        copy_button = ttk.Button(button_frame, text="Copy confirmed items", command=lambda: copy_to_clipboard(accepted_inventory, vendor_origins, True))
        copy_button.pack(side=tk.LEFT, padx=5)
    clear_button = ttk.Button(button_frame, text="Clear", command=reset)
    clear_button.pack(side=tk.LEFT, padx=5)

    message_frame.pack(fill=tk.BOTH, expand=True)


def hide_order_value_edit_section(hide=True):
    if hide:
        order_value_entry_us.pack_forget()
        change_button_us.pack_forget()
        order_value_entry_ca.pack_forget()
        change_button_ca.pack_forget()
    else:
        temp_order_value_us.set('')
        temp_order_value_ca.set('')
        order_value_entry_us.pack(side=tk.LEFT, padx=5)
        change_button_us.pack(side=tk.LEFT, padx=5)
        order_value_entry_ca.pack(side=tk.LEFT, padx=5)
        change_button_ca.pack(side=tk.LEFT, padx=5)


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    frame.pack_forget()


def clear_file_input(country):
    if country == 'us':
        file_path_us.set('')
    elif country == 'ca':
        file_path_ca.set('')


def update_browse_button(command):
    if command == 'us':
        if file_path_us.get():
            clear_file_button_us.pack(side=tk.LEFT, padx=5, pady=5)
            browse_button_us.pack_forget()
        else:
            browse_button_us.pack(side=tk.LEFT, padx=5, pady=5)
            clear_file_button_us.pack_forget()
    if command == 'ca':
        if file_path_ca.get():
            clear_file_button_ca.pack(side=tk.LEFT, padx=5, pady=5)
            browse_button_ca.pack_forget()
        else:
            browse_button_ca.pack(side=tk.LEFT, padx=5, pady=5)
            clear_file_button_ca.pack_forget()
    if command == 'process':
        browse_button_us.pack_forget()
        clear_file_button_us.pack_forget()
        browse_button_ca.pack_forget()
        clear_file_button_ca.pack_forget()



def reset():
    hide_order_value_edit_section(False)
    clear_frame(inventory_frame)
    clear_frame(message_frame)
    inventory_frame.pack_forget()
    message_frame.pack_forget()
    file_path_us.set('')
    file_path_ca.set('')
    process_button.pack(pady=10, before=separator)


def on_inner_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


def setup_gui():
    root = tk.Tk()
    root.title("Amazon Confirmation Processor")
    root.geometry('850x600')

    global file_path_us, file_entry_us, browse_button_us, clear_file_button_us
    global file_path_ca, file_entry_ca, browse_button_ca, clear_file_button_ca
    global min_order_value_us, temp_order_value_us
    global min_order_value_ca, temp_order_value_ca
    global process_button, separator
    global order_value_label_us, order_value_entry_us, change_button_us
    global order_value_label_ca, order_value_entry_ca, change_button_ca
    global inventory_frame, entries, canvas
    global message_frame

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
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Canvas
    canvas = tk.Canvas(main_frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add scrollbar to canvas
    scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure canvas
    canvas.configure(yscrollcommand=scrollbar.set)
    inner_main_frame = ttk.Frame(canvas)
    canvas_window = canvas.create_window((0, 0), window=inner_main_frame, anchor='nw')

    canvas.bind('<Configure>', lambda e: update_canvas_window(canvas, inner_main_frame, canvas_window))
    inner_main_frame.bind("<Configure>", lambda e: on_inner_frame_configure(e, canvas))
    

    # US Container Frame
    us_container_frame = ttk.Frame(inner_main_frame)
    us_container_frame.pack(pady=10)

    # US File Input Frame
    file_input_frame_us = ttk.Frame(us_container_frame, padding=5)
    file_input_frame_us.pack(side=tk.LEFT, padx=5)
    select_file_label_us = ttk.Label(file_input_frame_us, text="Amazon US File:")
    select_file_label_us.pack(side=tk.LEFT, padx=5, pady=5)
    file_entry_us = ttk.Entry(file_input_frame_us, textvariable=file_path_us, state='readonly', width=50, style='White.TEntry')
    file_entry_us.pack(side=tk.LEFT, padx=5, pady=5)
    browse_button_us = ttk.Button(file_input_frame_us, text="Browse", command=lambda: browse_files('us'))
    clear_file_button_us = ttk.Button(file_input_frame_us, text="Clear", command=lambda: clear_file_input('us'))

    # US Minimum Order Value Frame
    order_value_frame_us = ttk.Frame(us_container_frame, padding=5)
    order_value_frame_us.pack(side=tk.RIGHT, padx=5)
    order_value_label_us = ttk.Label(order_value_frame_us, text=f"Minimum Order Value: USD ${min_order_value_us.get()}")
    order_value_label_us.pack(side=tk.LEFT)
    order_value_entry_us = ttk.Entry(order_value_frame_us, textvariable=temp_order_value_us, width=4)
    order_value_entry_us.pack(side=tk.LEFT)
    change_button_us = ttk.Button(order_value_frame_us, text="Change", command=lambda: change_order_value('us'))
    change_button_us.pack(side=tk.LEFT)


    # CA Container Frame
    ca_container_frame = ttk.Frame(inner_main_frame)
    ca_container_frame.pack(pady=5)

    # CA File Input Frame
    file_input_frame_ca = ttk.Frame(ca_container_frame, padding=5)
    file_input_frame_ca.pack(side=tk.LEFT, padx=5)
    select_file_label_ca = ttk.Label(file_input_frame_ca, text="Amazon CA File:")
    select_file_label_ca.pack(side=tk.LEFT, padx=5, pady=5)
    file_entry_ca = ttk.Entry(file_input_frame_ca, textvariable=file_path_ca, state='readonly', width=50, style='White.TEntry')
    file_entry_ca.pack(side=tk.LEFT, padx=5, pady=5)
    browse_button_ca = ttk.Button(file_input_frame_ca, text="Browse", command=lambda: browse_files('ca'))
    clear_file_button_ca = ttk.Button(file_input_frame_ca, text="Clear", command=lambda: clear_file_input('ca'))

    # CA Minimum Order Value Frame
    order_value_frame_ca = ttk.Frame(ca_container_frame, padding=5)
    order_value_frame_ca.pack(side=tk.RIGHT, padx=5)
    order_value_label_ca = ttk.Label(order_value_frame_ca, text=f"Minimum Order Value: CAD ${min_order_value_ca.get()}")
    order_value_label_ca.pack(side=tk.LEFT)
    order_value_entry_ca = ttk.Entry(order_value_frame_ca, textvariable=temp_order_value_ca, width=4)
    order_value_entry_ca.pack(side=tk.LEFT)
    change_button_ca = ttk.Button(order_value_frame_ca, text="Change", command=lambda: change_order_value('ca'))
    change_button_ca.pack(side=tk.LEFT)

    # Browse/Clear Button
    file_path_us.trace_add('write', lambda *args: update_browse_button('us'))
    file_path_ca.trace_add('write', lambda *args: update_browse_button('ca'))
    update_browse_button('us')
    update_browse_button('ca')

    # Process Button
    process_button = ttk.Button(inner_main_frame, text="Process", command=process_files)
    process_button.pack(pady=10)

    # Separator for visual distinction
    separator = ttk.Separator(inner_main_frame)
    separator.pack(fill=tk.X, pady=(10, 10))

    # Inventory Frame
    inventory_frame = ttk.Frame(inner_main_frame)
    inventory_frame.grid_columnconfigure(0, weight=1, minsize=150)
    inventory_frame.grid_columnconfigure(1, weight=1, minsize=150)
    inventory_frame.grid_columnconfigure(2, weight=1, minsize=150)

    # Message Frame
    message_frame = ttk.Frame(inner_main_frame)
    message_frame.grid_columnconfigure(0, weight=1, minsize=450)

    root.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all")) 

    root.mainloop()


def update_canvas_window(canvas, frame, canvas_window):
    new_width = canvas.winfo_width()
    canvas.itemconfig(canvas_window, width=new_width)  
    frame.update_idletasks()  
    adjust_frame_center(canvas, frame, canvas_window)


def adjust_frame_center(canvas, frame, canvas_window):
    canvas_width = canvas.winfo_width()
    frame_width = frame.winfo_reqwidth()
    coord_x = max((canvas_width - frame_width) // 2, 0)
    canvas.coords(canvas_window, coord_x, 0)
    canvas.configure(scrollregion=canvas.bbox("all"))


def on_inner_frame_configure(event, canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))


if __name__ == "__main__":
    setup_gui()
