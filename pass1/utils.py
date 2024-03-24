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


def calculate_fine_amount(land_id, new_duration, land_info):
    """
    Calculate the remaining rent amount based on the newly entered duration and rented duration.
    """
    rented_duration = 0
    rented_price = 0
    fine_percent = 0.1
    total=0
    
    # Read rental information for the specified land
    with open("data/rental_info.txt", 'r') as file:
        for line in file:
            try:
                line_land_id, duration = map(int, line.strip().split(','))
                if line_land_id == land_id and land_id in land_info:
                    rented_duration += duration
                    rented_price += land_info[land_id]['price'] * duration
            except ValueError:
                print(f"Error reading line: {line}. Skipping...")
    
    # Calculate remaining duration
    remaining_duration = new_duration - rented_duration
    
    if(remaining_duration>0):
        fine = (new_duration - rented_duration) * land_info[land_id]['price'] * fine_percent
    else:
        fine = 0
    total = (rented_duration) * land_info[land_id]['price'] + fine
    return fine,total


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
