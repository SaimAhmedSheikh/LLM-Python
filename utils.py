import re, json

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
