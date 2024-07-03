from utils import  read_data, write_data_to_file

test_results = read_data('test_results.json')
explanations = read_data('explanations.json')


def find_summary(patient_data):
    for i in range(0, len(explanations)):
        explanation = explanations[i]
        explan_patient_data = explanation['patient_data']
        if patient_data == explan_patient_data:
            return explanation['summary']
    return None


combined_data = []
combined = {}
for i in range(0, len(test_results)):
    test_result = test_results[i]
    patient_data = test_result['patient_data']
    summary = find_summary(patient_data)
    if summary is not None and summary != "":
        combined = {}
        combined['filename'] = test_result['filename']
        combined['patient_data'] = patient_data
        combined['test_results'] = test_result['results']
        combined['summary'] = summary
        combined_data.append(combined)

output_file_path = "combined.json"
write_data_to_file(combined_data, output_file_path)
print(f"Data has been written to {output_file_path}")
print(f"Number of files: {len(combined_data)}")
