import pdfplumber, json, glob, os
import pandas as pd
from utils import get_numerical_values

PATIENT_DATA_KEYS = [
    "Surname",
    "Forename",
    "Date of birth",
    "Sample Number",
    "Sex",
    "Lab No",
    "Sample Dated",
    "Sample Received",
    "Result Reported",
    "Sample Type",
    ]

def extract_info(entry=[], test_name=""):
    test_name_parts = []
    value = None
    hi_low = None
    range_parts = []
    comment_parts = []

    # Traverse the entry until the first numerical value
    if len(entry) > 0:
        for item in entry:
            if value is None and item.replace('.', '', 1).isdigit():
                value = item
            elif value is None:
                if item == "H" or item == "L":
                    hi_low = item
                else:
                    test_name_parts.append(item)
            else:
                test_value_index = entry.index(value)
                range_parts = entry[test_value_index+1:]
                # After the test value, we gather range and units
                # if '-' in result:
                #     range_index = entry.index('-')
                #     range_parts = entry[range_index - 1:]
                # else:
                #     range_parts.append(item)
                if "New" in range_parts:
                    comments_index = range_parts.index("New")
                    comment_parts = range_parts[comments_index:]
                    range_parts = range_parts[:comments_index]

    
    paramter = " ".join(test_name_parts)
    test_range = " ".join(range_parts)
    comments = " ".join(comment_parts)

    if paramter == "" or value == None or test_range == "":
        return None
    return {
        "Test Name": test_name,
        "Parameter": paramter,
        "Value": value,
        "Range": test_range,
        "Comments": comments,
        "H/L": hi_low,
    }

def extract_and_parse_pdf(file_path):
    lines = []
    try:
        with pdfplumber.open(file_path) as pdf:
            pageStarted = False
            for page in pdf.pages:
                pageData = page.extract_text_lines(layout=True, strip=True, return_chars=False)
                textLines = [line['text'] for line in pageData]
                noLines = len(textLines)
                for i in range(0,noLines):
                    line = textLines[i]
                    if "Surname" in line:
                        pageStarted = True
                    elif "page" in line.lower():
                        pageStarted = False
                    if pageStarted == True:
                        lines.append(line)
    except Exception as e:
        print("An exception occurred: ", e)
        return lines
    else:
        print("*** Pdf processed successfully ***")
    
    
    newLines = lines.copy()

    # # Initialize a dictionary to hold the extracted data
        
    patientData = {}

    for line in newLines:
        if(":" in line):
            if "Surname" in line:
                patientData["surname"] = line.split(":")[1].strip()
            elif "Forename" in line:
                patientData["forename"] = line.split(":")[1].strip()
            elif "Date of birth" in line:
                patientData["date_of_birth"] = line.split(":")[1].strip()
            elif "Sample Number" in line:
                patientData["sample_number"] = line.split(":")[1].strip()
            elif "Sex" in line:
                patientData["sex"] = line.split(":")[1].strip()
            elif "Lab No" in line:
                patientData["lab_no"] = line.split(":")[1].strip()
            elif "Sample Dated" in line:
                patientData["sample_dated"] = line.split(":")[1].strip()
            elif "Sample Received" in line:
                patientData["sample_received"] = line.split(":")[1].strip()
            elif "Result Reported" in line:
                patientData["result_reported"] = line.split(":")[1].strip()
            elif "Sample Type" in line:
                patientData["sample_type"] = line.split(":")[1].strip()

    
    newLines = [line for line in newLines if not any(word in line for word in PATIENT_DATA_KEYS)]
    newLines = [line for line in newLines if not any(word in line for word in ["Test", "Result", "Range", "Comment"])]

    results = []
    test_name = None

    if len(newLines) > 0:
        for line in newLines:
            values = line.split(" ")
            values = [value.strip() for value in values]
            values = [value for value in values if value != ""]
            numbers = get_numerical_values(line)
            if len(numbers) == 0 and test_name == None:
                test_name = line
            else:
                result = extract_info(values, test_name)
                if result != None:
                    results.append(result)


    # length = len(newLines)
    # results = []
    # result = None
    # for i in range(0, length):
    #     line = newLines[i]
    #     nextLine = newLines[i+1] if i+1 < length else None
    #     if nextLine is not None and "Result" in nextLine:
    #         results.append(result) if result is not None else None
    #         result = []
    #     elif nextLine is None and i == length-1:
    #         results.append(result) if result is not None else None
    #     if result is not None:
    #         result.append(line)
    #         newLines2.remove(line)

    # resultData = []
    # for result in results:
    #     resultData.append({
    #         "test": result[0],
    #         "result": result[1],
    #         "range": result[2],
    #         "explanation": " ".join(result[3:]) if len(result) > 3 else None,
    #     })

    # summaryLines = newLines2.copy()
    # summary = " ".join(summaryLines[1:])
    # print(summary)
        
    # data = {
    #     "patient_data": patientData,
    #     "results": resultData,
    #     "summary": summary,
    # }
    # print(patientData)
    # print(results)
    return { "patient_data": patientData, "results": results }

def write_data_to_file(data, output_file):
    with open(output_file, 'w') as file:
        file.write(json.dumps(data, indent=2))

def write_data_to_csv(data, output_file):
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)

    
# Path to the directory
directory_path = 'sample_results'
# List all files matching the pattern
files = os.listdir(directory_path)
test_results = []

# Loop through the files and read them
for filename in files:
    file_path = os.path.join(directory_path, filename)
    print(file_path)
    if os.path.isfile(file_path):  # Check if it is a file
        result = extract_and_parse_pdf(file_path)
        filename = filename.split(".")[0]
        test_results.append({ "file_name": filename, "result": result })
        # write_data_to_file(parsed_data, file_path.split(".")[0]+".json")
        # allData.append(result)
        # output_file_path = file_path.split(".")[0]+".json"

output_file_path = "result_data.json"
write_data_to_file(test_results, output_file_path)
print(f"Data has been written to {output_file_path}")
output_file_path = "result_data.csv"
write_data_to_csv(test_results, output_file_path)
print(f"Data has been written to {output_file_path}")
