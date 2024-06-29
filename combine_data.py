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


data = []
combined = {}
for i in range(0, len(test_results)):
    test = test_results[i]
    patient_data = test['patient_data']
    summary = find_summary(patient_data)
    if summary:
        combined['patient_data'] = patient_data
        combined['test_results'] = test['results']
        combined['summary'] = summary
        data.append(combined)

output_file_path = "combined.json"
write_data_to_file(data, output_file_path)
print(f"Data has been written to {output_file_path}")
print(f"Number of files: {len(data)}")
