def review_inventory(accepted_inventory, original_path, min_order_value):
    print("Original Path:", original_path)
    print("\nAccepted Inventory:")
    print("-" * 40)
    print("{:<15} | {:>10}".format("Model Number", "Quantity"))
    print("-" * 40)
    for model, quantity in accepted_inventory.items():
        print("{:<15} | {:>10}".format(model, quantity))
    print("-" * 40)


def convert_xlsx_to_xls(src_file_path, dst_file_path):
    print('hi')

