import re

def feet_inches_to_meters(input_string):
    feet_inches_pattern = r'(\d+)\s*\'\s*(\d+)\s*\"'
    match = re.search(feet_inches_pattern, input_string)
    if match:
        feet = int(match.group(1))
        inches = int(match.group(2))
        meters = (feet * 0.3048) + (inches * 0.0254)
        return meters
    else:
        return None
    

def meters_to_meters(input_string):
    meters_pattern = r'(\d+(\.\d+)?)\s*m'
    match = re.search(meters_pattern, input_string)
    if match:
        meters = float(match.group(1))
        return meters
    else:
        return None
    

def feet_only_to_meters(input_string):
    feet_only_pattern = r'(\d+)\s*\''
    match = re.search(feet_only_pattern, input_string)
    if match:
        feet = int(match.group(1))
        meters = feet * 0.3048
        return meters
    else:
        return None
    

def decimal_feet_to_meters(input_string):
    decimal_feet_pattern = r'(\d+(\.\d+)?)\s*feet?'
    match = re.search(decimal_feet_pattern, input_string)
    if match:
        feet = float(match.group(1))
        meters = feet * 0.3048
        return meters
    else:
        return None
    

def decimal_feet_contracted_to_meters(input_string):
    decimal_feet_pattern = r'(\d+(\.\d+)?)\s*ft?'
    match = re.search(decimal_feet_pattern, input_string)
    if match:
        feet = float(match.group(1))
        meters = feet * 0.3048
        return meters
    else:
        return None

def feet_inches_dot_to_meters(input_string):
    pattern = r'(\d+)\s*ft\.\s*(\d+)\s*in\.'
    match = re.search(pattern, input_string)
    if match:
        feet = int(match.group(1))
        inches = int(match.group(2))
        meters = (feet * 0.3048) + (inches * 0.0254)
        return meters
    else:
        return None
    

def extract_float_from_european_number(text):
    pattern = r'(\d+,\d+)\s*m'
    match = re.search(pattern, text)
    if match:
        num_str = match.group(1)
        num_str = num_str.replace(',', '.')
        return float(num_str)
    else:
        return None
    

def ft_to_metres(input_string):
    pattern = r'(\d+)\s*ft'
    match = re.search(pattern, input_string)
    if match:
        feet = int(match.group(1))
        meters = feet * 0.3048
        return meters
    else:
        return None
    

def feet_inches_to_meters2(input_string):
    pattern = r'\b(\d+)\'(\d+)\s*ft\b'
    match = re.search(pattern, input_string)
    if match:
        feet = int(match.group(1))
        inches = int(match.group(2))
        meters = (feet * 0.3048) + (inches * 0.0254)
        return meters
    else:
        return None

def slash_separated_to_meters(input_string):
    pattern = r'(\d+(\.\d+)?)\s*/\s*(\d+(\.\d+)?)'
    match = re.search(pattern, input_string)
    if match:
        feet = float(match.group(1))
        meters = feet * 0.3048
        return meters
    else:
        return None

def identify_and_extract_boat_length_format(input_string):
    try:
        return float(input_string)
    except:
        pass
    # Format: Feet and Inches (e.g., "25 feet 6 inches")
    feet_inches_pattern = r'(\d+)\s*\'\s*(\d+)\s*\"'

    # Format: Meters (e.g., "7.5 meters" or "7.5m")
    meters_pattern = r'(\d+(\.\d+)?)\s*m'

    # Format: Feet Only (e.g., "30 feet" or "30'")
    feet_only_pattern = r'(\d+)\s*\''

    # Format: Decimal Feet (e.g., "25.5 feet")
    decimal_feet_pattern = r'(\d+(\.\d+)?)\s*feet?'

    # Format: Decimal Feet contracted (e.g., "25.5 ft")
    decimal_feet_contracted_pattern = r'\d+\.\d+\s*ft?'

    feet_inches_dot_pattern = r'(\d+)\s*ft\.\s*(\d+)\s*in\.'

    european_metres = r'\d+,\d+\s*m'

    ft_to_metres_pattern = r'(\d+)\s*ft'

    ft_to_metres_pattern2 = r'\b(\d+)\'(\d+)\s*ft\b'

    slash_separated_pattern = r'(\d+(\.\d+)?)\s*/\s*(\d+(\.\d+)?)'

    # Check each pattern
    if re.search(feet_inches_pattern, input_string):
        return feet_inches_to_meters(input_string)
    elif re.search(meters_pattern, input_string) and ',' not in input_string:
        return meters_to_meters(input_string)
    elif re.search(feet_only_pattern, input_string):
        return feet_only_to_meters(input_string)
    elif re.search(decimal_feet_pattern, input_string):
        return decimal_feet_to_meters(input_string)
    elif re.search(decimal_feet_contracted_pattern, input_string):
        return decimal_feet_contracted_to_meters(input_string)
    elif re.search(feet_inches_dot_pattern, input_string):
        return feet_inches_dot_to_meters(input_string)
    elif re.search(european_metres, input_string):
        return extract_float_from_european_number(input_string)
    elif re.search(ft_to_metres_pattern, input_string):
        return ft_to_metres(input_string)
    elif re.search(ft_to_metres_pattern2, input_string):
        return feet_inches_to_meters2(input_string)
    elif re.search(slash_separated_pattern, input_string):
        return slash_separated_to_meters(input_string)
    else:
        return None
