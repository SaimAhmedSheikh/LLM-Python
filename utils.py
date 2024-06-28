import re

def get_numerical_values(s):
    # Regular expression to match numerical values
    pattern = r'\d+(\.\d+)?'
    return re.findall(pattern, s)
