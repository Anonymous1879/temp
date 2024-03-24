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
