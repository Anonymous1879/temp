from invoice import generate_invoice_string
from display import display_all_lands
from utils import save_land_info, save_rental_info
import datetime

def rent_land(land_info):
    while True:
        display_all_lands(land_info)
        customer_name = input("Enter customer name: ")

        rented_lands = []
        while True:
            land_id_input = input("Enter land ID to rent (or 'done' to finish): ")
            if land_id_input.lower() == 'done':
                break
            if land_id_input.strip().isdigit():
                land_id = int(land_id_input)
                if land_id in land_info and land_info[land_id]['status'].strip() == 'Available':
                    duration_input = input(f"Enter duration of rent for land {land_id} (in months): ")
                    if duration_input.isdigit() and int(duration_input) > 0:
                        rented_lands.append((land_id, int(duration_input)))
                    else:
                        print("Invalid duration. Please enter a positive integer value.")
                else:
                    print(f"Invalid input or land {land_id} is not available. Please try again or enter 'done' to finish.")

        if rented_lands:
            customer_invoice_string = f"\nInvoice for {customer_name}:\n"
            total_amount = 0
            for land_id, duration in rented_lands:
                land = land_info[land_id]
                total_amount += land['price'] * duration
                customer_invoice_string += f"\nLand ID: {land_id}\n"
                customer_invoice_string += generate_invoice_string(customer_name, land_id, land, duration, land['price'] * duration)
                customer_invoice_string += "\n"
                # Update land status to 'Not Available'
                land_info[land_id]['status'] = 'Not Available'
                # Save the duration information
                save_rental_info("data/rental_info.txt", {land_id: duration})

            # Save the updated land_info
            save_land_info("data/land_info.txt", land_info)
            
            # Generate file name based on the customer's name, current date, and time
            current_datetime = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
            file_name = f"{customer_name}_{current_datetime}_rent_invoice.txt"
            with open(file_name, 'w') as file:
                file.write(customer_invoice_string)
            
            print(customer_invoice_string)
            print(f"Invoice has been saved as '{file_name}'")
        else:
            print("No valid lands selected for rent.")

        choice = input("Do you want to rent another land? (yes/no): ")
        if choice.lower() != 'yes':
            break 
