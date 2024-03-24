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
    invoice_string += f"Fine Amount: NPR {fine_amount}\n"
    invoice_string += f"Total Amount: NPR {total_amount}\n"
    invoice_string += f"{'=' * 40}\n"
    invoice_string += f"Thank you for your business!\n"
    invoice_string += f"{'=' * 40}\n"
    return invoice_string


def display_invoice(customer_name, land_id, land_details, duration, total_rent_amount, fine_amount):
    invoice_string = generate_invoice_string(customer_name, land_id, land_details, duration, total_rent_amount, fine_amount)
    print(invoice_string)
