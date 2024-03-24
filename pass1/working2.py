def display_table(data, headers):
    print("-" * 56)
    print(" | ".join(headers))
    print("-" * 56)
    for row in data:
        print(" | ".join(str(item) for item in row))
    print("-" * 56)

# display.py

def display_all_lands(land_info):
    print("Available Lands:")
    
    available_lands = [[kitta, details['city'], details['direction'], details['area'], details['status'].strip()]
                       for kitta, details in land_info.items() if details['status'].strip() == 'Available']

    if available_lands:
        display_table(available_lands, ["Kitta", "City", "Direction", "Area", "Status"])
    else:
        print("No available lands.")

    print("\nRented Lands:")
    rented_lands = [[kitta, details['city'], details['direction'], details['area'], details['status'].strip()]
                    for kitta, details in land_info.items() if details['status'].strip() == 'Not Available']
    if rented_lands:
        display_table(rented_lands, ["Kitta", "City", "Direction", "Area", "Status"])
    else:
        print("No lands are currently rented out.")



def display_starting_page():
    print("**********************************************************")
    print("*              Welcome to TechnoPropertyNepal            *")
    print("*                 Land Renting System                    *")
    print("**********************************************************")
    print("This system allows you to rent and return lands.")
    print("You can also generate and print invoices for rented lands.")
    print("\nPlease select an option from the menu below to proceed:")
    print("1. Rent land")
    print("2. Return land")
    print("3. Exit")
    print("**********************************************************")


# invoice.py
import datetime

def generate_invoice_string(customer_name, land_id, land_details, duration, total_amount, fine_amount=0):
    invoice_string = f"{'=' * 40}\n"
    invoice_string += f"TechnoPropertyNepal\n"
    invoice_string += f"Land Rental Invoice\n"
    invoice_string += f"{'=' * 40}\n"
    invoice_string += f"Customer Name: {customer_name}\n"
    invoice_string += f"Kitta Number: {land_id}\n"
    invoice_string += f"City: {land_details['city']}\n"
    invoice_string += f"Direction: {land_details['direction']}\n"
    invoice_string += f"Date and Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    invoice_string += f"{'=' * 40}\n"
    invoice_string += f"Duration of Rent: {duration} months\n"
    invoice_string += f"Individual Rent Price per Month: NPR {land_details['price']}\n"
    start_date = datetime.datetime.now()
    end_date = start_date + datetime.timedelta(days=int(duration) * 30)
    invoice_string += f"Start Date: {start_date.strftime('%Y-%m-%d')}\n"
    invoice_string += f"End Date: {end_date.strftime('%Y-%m-%d')}\n"
    invoice_string += f"{'=' * 40}\n"
    invoice_string += f"Total Amount: NPR {total_amount}\n"
    invoice_string += f"Fine Amount: NPR {fine_amount}\n"
    invoice_string += f"{'=' * 40}\n"
    invoice_string += f"Thank you for your business!\n"
    invoice_string += f"{'=' * 40}\n"
    return invoice_string


def display_invoice(customer_name, land_id, land_details, duration, total_rent_amount, fine_amount):
    invoice_string = generate_invoice_string(customer_name, land_id, land_details, duration, total_rent_amount, fine_amount)
    print(invoice_string)


from invoice import generate_invoice_string
from display import display_all_lands
from utils import save_land_info, save_rental_info, read_rental_info
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


# return_operations.py

from invoice import generate_invoice_string
from display import display_all_lands
from utils import save_land_info, read_rental_info, delete_returned_lands_info, calculate_fine_amount
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
                
                # Calculate fine amount only if rented duration exceeds specified duration
                if duration > land.get('rented_duration', 0):
                    fine_amount = calculate_fine_amount(land, duration)
                else:
                    fine_amount = 0
                
                customer_invoice_string += f"\nLand ID: {land_id}\n"
                customer_invoice_string += generate_invoice_string(customer_name, land_id, land, duration, 0, fine_amount)  # Set total_amount to 0 for return operation
                customer_invoice_string += "\n"

            # Save the updated land_info
            save_land_info("data/land_info.txt", land_info)
            
            # Remove the rental information from rental_info file for returned lands
            rental_info = read_rental_info("data/rental_info.txt")
            for land_id, duration in returned_lands:
                if land_id in rental_info:
                    del rental_info[land_id]

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


# utils.py

def save_land_info(file_path, land_info):
    """
    Save land information to a file.
    """
    with open(file_path, 'w') as file:
        for land_id, details in land_info.items():
            status = details.get('status', 'Available')
            file.write(f"{land_id},{details['city']},{details['direction']},{details['area']},{details['price']},{status}\n")

def read_land_info(file_path):
    land_info = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:  # Skip empty lines
                try:
                    land_id, city, direction, area, price, status = line.split(',')
                    land_info[int(land_id)] = {
                        'city': city,
                        'direction': direction,
                        'area': float(area),
                        'price': float(price),
                        'status': status
                    }
                except ValueError:
                    print(f"Error reading line: {line}. Skipping...")
    # print(land_info)
    return land_info


# utils.py
def save_rental_info(file_path, rental_info):
    """
    Save rental information to a file.
    """
    with open(file_path, 'a') as file:
        for land_id, duration in rental_info.items():
            file.write(f"{land_id},{duration}\n")



def read_rental_info(file_path):
    """
    Read rental information from a file.
    """
    rental_info = {}
    with open(file_path, 'r') as file:
        for line in file:
            try:
                land_id, duration = map(int, line.strip().split(','))
                rental_info[land_id] = duration
            except ValueError:
                print(f"Error reading line: {line}. Skipping...")

    return rental_info

def calculate_fine_amount(land, duration):
    # Calculate fine amount as 10% of rent per month
    fine_percentage = 0.10
    rent_per_month = land['price']
    fine_amount = 0
    if duration > land.get('rented_duration', 0):
        fine_amount = fine_percentage * rent_per_month * (duration - land.get('rented_duration', 0))
    return fine_amount

def delete_returned_lands_info(file_path, returned_lands):
    """
    Delete the information of returned lands from the rental_info file.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            land_id = int(line.split(',')[0])
            if land_id not in returned_lands:
                file.write(line)


# main.py

from display import display_starting_page
from rent_operations import rent_land
from return_operations import return_land
from utils import read_land_info, save_land_info
def main():
    land_info = read_land_info("data/land_info.txt")
    if not land_info:
        print("Error: Unable to read land information from file.")
        return

    while True:
        display_starting_page()
        choice = input("Enter your choice: ")
        if choice == '1':
            rent_land(land_info)
        elif choice == '2':
            return_land(land_info)
        elif choice == '3':
            save_land_info("data/land_info.txt", land_info)
            print("Exiting program...")
            break
        else:
            print("Invalid choice! Please enter a valid option.")

    save_land_info("data/land_info.txt", land_info)

if __name__ == "__main__":
    main()