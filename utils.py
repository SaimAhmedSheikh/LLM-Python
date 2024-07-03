import re, json, csv
import pandas as pd

def get_numerical_values(s):
    # Regular expression to match numerical values
    pattern = r'\d+(\.\d+)?'
    return re.findall(pattern, s)

def read_data(filepath):
    # Open and read the JSON file
    with open(filepath, 'r') as f:
        data = f.read()

    # Convert JSON data to a dictionary
    try:
        json_dict = json.loads(data)
        return json_dict
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None


def write_data_to_file(data, output_file):
    with open(output_file, 'w') as file:
        file.write(json.dumps(data, indent=2))

def write_data_to_csv(json_data, csv_file_path):
    # Ensure json_data is a list of dictionaries
    if isinstance(json_data, str):
        json_data = json.loads(json_data)

    # Check if the json_data is a list of dictionaries
    if not isinstance(json_data, list):
        raise ValueError("JSON data should be a list of dictionaries")

    # Open the CSV file for writing
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        # Create a CSV DictWriter object
        writer = csv.DictWriter(csv_file, fieldnames=json_data[0].keys(), delimiter='|')
        
        # Write the header
        writer.writeheader()
        
        # Write the data rows
        for row in json_data:
            writer.writerow(row)

def extract_substring(input_string, keyword):
    # Use regular expression to find the substring "White Blood Cells"
    match = re.search(re.escape(keyword), input_string)
    if match:
        return match.group(0)
    else:
        return None

def find_first_number(input_string):
    # Use regular expression to find the first occurrence of a numerical value
    match = re.search(r"\d+(\.\d+)?", input_string)
    if match:
        return match.group(0)
    else:
        return None
