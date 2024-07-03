import pdfplumber, json, glob, os
import pandas as pd
from utils import get_numerical_values, write_data_to_csv, write_data_to_file, extract_substring, find_first_number

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

RESULTS_DATA_KEYS = [
    'CRP',
    'Albumin',
    'CK',
    'Iron',
    'Total Protein',
    'Globulin',
    'Ferritin',
    'HbA1c-(IFCC)',
    'T.I.B.C',
    'Transferrin Saturation',
    'Chloride',
    'Calcium',
    'Glucose',
    'Potassium',
    'Magnesium',
    'Uric Acid',
    'Haemoglobin',
    'Red Blood Cell',
    'Haematocrit',
    'Mean Cell Volume',
    'Red Cell Distribution',
    'Mean Cell Hb',
    'MCHC',
    'Platelets',
    'MPV',
    'White Blood Cells',
    'Neutrophils',
    'Monocytes',
    'Basophils',
    'Eosinophils',
    'Lymphocytes',
    'Cortisol',
    'Prolactin',
    'Oestradiol',
    'Progesterone',
    'LH',
    'FSH',
    'DHEA-S',
    'SHBG',
    'LH',
    'FSH',
    'Oestradiol',
    'Ovulation',
    'Luteal',
    'Progesterone',
    'Periovulatory',
    'Postmenopause',
    'Testosterone',
    'SHBG',
    'Anti-Thyroglobulin Abs',
    'Anti-Thyroidperoxidase abs',
    'Urea',
    'Creatinine',
    'Sodium',
    'eGFR (Caucasian Only)',
    'Cystatin C',
    'Cholesterol',
    'HDL',
    'LDL',
    'Triglycerides',
    'Non HDL Cholesterol',
    'Chol: HDL ratio',
    'GGT',
    'ALP',
    'ALT',
    'Total Bilirubin',
    'AST',
    'Total PSA',
    'Free T4',
    'TSH',
    'Free T3',
    'Vitamin B12',
    'Vitamin D 3',
    'Folate',
    'Vitamin B12',
]
TEST_NAMES = [
    'Biochemistry',
    'Bone Screen',
    'Full Blood Count',
    'Hormones',
    'Immunology',
    'Kidney Function',
    'Lipids',
    'Liver Function',
    'Markers',
    'Thyroid Function',
    'Vitamins',
]
def extract_results(line, test_name="", parameter_name=""):
    value = ""
    hi_low = None
    range_parts = []
    comment_parts = []

    values = line.split(" ")
    values = [value.strip() for value in values]
    values = [value for value in values if value != ""]

    if "H" in values:
        hi_low = values.pop(values.index("H"))
    if "L" in values:
        hi_low = values.pop(values.index("L"))
    if "LL" in values:
        hi_low = values.pop(values.index("LL"))
    if "HH" in values:
        hi_low = values.pop(values.index("HH"))

    # Traverse the entry until the first numerical value

    newLine = " ".join(values)
    value = find_first_number(newLine)
    remaining = ""
    if value is not None:
        valueIndex = newLine.find(value)
        if valueIndex != -1:
            remaining = newLine[:valueIndex]
        if remaining != "":
            if ">" in remaining:
                value = ">" + value
            elif "<" in remaining:
                value = "<" + value
            elif ">=" in remaining:
                value = ">=" + value
            elif "<=" in remaining:
                value = "<=" + value

        newLine = newLine.replace(remaining, "")
        newLine = newLine.replace(value, "")

    test_range = newLine.strip()

    if parameter_name == "" or value == "" or test_range == "":
        return None
    return {
        "Test Name": test_name,
        "Parameter": parameter_name,
        "Value": value,
        "Range": test_range,
        "H/L": hi_low,
    }

count = 0
def extract_summary(newLines=[]):
    newLines2 = newLines.copy()

    length = len(newLines)
    results = []
    result = None
    for i in range(0, length):
        line = newLines[i]
        nextLine = newLines[i+1] if i+1 < length else None
        if nextLine is not None and nextLine.startswith("Result"):
            results.append(result) if result is not None else None
            result = []
        elif nextLine is None and i == length-1:
            results.append(result) if result is not None else None
        if result is not None:
            result.append(line)
            newLines2.remove(line)

    resultData = []
    for result in results:
        resultData.append({
            "test": result[0] if len(result) > 0 else None,
            "result": result[1] if len(result) > 1 else None,
            "range": result[2] if len(result) > 2 else None,
            "explanation": " ".join(result[3:]) if len(result) > 3 else None,
        })

    summaryLines = newLines2.copy()
    summary = " ".join(summaryLines[1:])
    # print(summary)
        
    data = {
        "explanations": resultData,
        "summary": summary,
    }
    # print(patientData)
    # print(results)
    return data

def extract_lines(file_path):
    textLines = []
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                pageData = page.extract_text_lines(layout=False, strip=True, return_chars=False)
                textLines.extend([line['text'] for line in pageData])
    except Exception as e:
        print("An exception occurred: ", e)
        return textLines
    else:
        print("*** Pdf processed successfully ***")
        return textLines
    

def extract_and_parse_pdf(file_path, filename=""):
    textLines = extract_lines(file_path)
    isExplanation = False

    for line in textLines:
        words = line.split(" ")
        if "Report" in words and "Explanation" in words:
            isExplanation = True
            break

    n = len(textLines)
    pageStarted = False
    lines = []
    for i in range(0,n):
        line = textLines[i]
        if "Surname" in line:
            pageStarted = True
        elif "page" in line.lower():
            pageStarted = False
        if pageStarted == True:
            lines.append(line)
    
    lines = [line for line in lines if not "Results generated by" in line]

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
    
    if isExplanation == False:
        newLines = [line for line in newLines if not any(word in line for word in ["Result", "Range", "Units"])]
        results = []
        test_name = None
        if len(newLines) > 0:
            for line in newLines:
                for key in TEST_NAMES:
                    if key in line:
                        test_name = key
                        break
                parameter_name = None
                for key in RESULTS_DATA_KEYS:
                    if key in line:
                        parameter_name = key
                        break
                if parameter_name == None:
                    continue
                line = line.replace(parameter_name, "")
                # print(test_name)
                result = extract_results(line, test_name, parameter_name)
                if result != None:
                    results.append(result)

        return { "filename": filename, "isExplanation": isExplanation, "patient_data": patientData, "results": results  }
    else:
        data = extract_summary(newLines)
        return { "filename": filename, "isExplanation": isExplanation, "patient_data": patientData, "explanations": data["explanations"], "summary": data["summary"] }



# Path to the directory
directory_path = 'reports'
# List all files matching the pattern
files = os.listdir(directory_path)
test_results = []
explanations = []
# Loop through the files and read them
for filename in files:
    file_path = os.path.join(directory_path, filename)
    print(file_path)
    if os.path.isfile(file_path):  # Check if it is a file
        count += 1
        result = extract_and_parse_pdf(file_path, filename=filename.split(".")[0])
        if result["isExplanation"] == False:
            test_results.append(result)
        else:
            explanations.append(result)

print(f"Number of files found: {count}")

output_file_path = "test_results.json"
write_data_to_file(test_results, output_file_path)
print(f"Data has been written to {output_file_path}")
print(f"Number of results files: {len(test_results)}")

output_file_path = "explanations.json"
write_data_to_file(explanations, output_file_path)
print(f"Data has been written to {output_file_path}")
print(f"Number of explanation files processed: {len(explanations)}")

