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


def write_data_to_file(data, output_file):
    with open(output_file, 'w') as file:
        file.write(json.dumps(data, indent=2))

def write_data_to_csv(data, output_file):
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
