
def assemble_address(street_number, street_name, street_suffix, city, unit, state, zip_code):
    # Components of the address
    if unit:
        address = f"{street_number} {street_name} {street_suffix}, {unit}, {city}, {state} {zip_code}"
    else:
        address = f"{street_number} {street_name} {street_suffix}, {city}, {state} {zip_code}"
    
    return address.strip()

def assemble_name(first_name, middle_name, last_name):
    if middle_name:
        return f"{first_name} {middle_name} {last_name}".strip()
    else:
        return f"{first_name} {last_name}".strip()
