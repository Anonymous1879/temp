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
