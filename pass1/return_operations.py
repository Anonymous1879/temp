# return_operations.py

from invoice import generate_invoice_string
from display import display_all_lands
from utils import  delete_returned_lands_info, calculate_fine_amount
import datetime

def return_land(land_info):
    while True:
        display_all_lands(land_info)

        rented_land_ids = [int(land_id) for land_id in land_info if land_info[land_id]['status'].strip() == 'Not Available']
        print("Rented Land IDs:", rented_land_ids)

        if not rented_land_ids:
            print("No lands are currently rented out.")
            break

        customer_name = input("Enter customer name: ")

        returned_lands = []
        while True:
            land_id_input = input("Enter land ID to return (or 'done' to finish): ")
            if land_id_input.lower() == 'done':
                break
            if land_id_input.strip().isdigit():
                land_id = int(land_id_input)
                if land_id in land_info and land_info[land_id]['status'].strip() == 'Not Available':
                    duration_input = input(f"Enter duration of rent for land {land_id} (in months): ")
                    if duration_input.isdigit() and int(duration_input) > 0:
                        returned_lands.append((land_id, int(duration_input)))
                    else:
                        print("Invalid duration. Please enter a positive integer value.")
                else:
                    print(f"Invalid input or land {land_id} is not available. Please try again or enter 'done' to finish.")

        if returned_lands:
            customer_invoice_string = f"\nInvoice for {customer_name}:\n"
            for land_id, duration in returned_lands:
                land_info[land_id]['status'] = 'Available'  # Update land status
                land = land_info[land_id]

                fine_amount,total = calculate_fine_amount(land_id, duration, land_info)
                
                customer_invoice_string += f"\nLand ID: {land_id}\n"
                customer_invoice_string += generate_invoice_string(customer_name, land_id, land, duration, total, fine_amount)  # Set total_amount to 0 for return operation
                customer_invoice_string += "\n"

            delete_returned_lands_info("data/rental_info.txt", [land_id for land_id, _ in returned_lands])

            
            # Generate file name based on the customer's name, current date, and time
            current_datetime = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
            file_name = f"{customer_name}_{current_datetime}_return_invoice.txt"
            with open(file_name, 'w') as file:
                file.write(customer_invoice_string)
            
            print(customer_invoice_string)
            print(f"Invoice has been saved as '{file_name}'")
        else:
            print("No lands selected for return.")

        choice = input("Do you want to return another land? (yes/no): ")
        if choice.lower() != 'yes':
            break
