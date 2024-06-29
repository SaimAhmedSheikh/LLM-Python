from utils import  read_data, write_data_to_csv

data = read_data('combined.json')

csv_data = []

for i in range(0, len(data)):
    item = data[i]
    test_results = item['test_results']
    summary = item['summary']
    values = []
    for test in test_results:
        if(test['Parameter'] == ""):
            continue
        if(test['Value'] == ""):
            continue
        values.append(f"{test['Parameter']}:{test['Value']}")
    csv_data.append({
        "Results": ", ".join(values),
        "Summary": summary
    })

output_file_path = "results.csv"
write_data_to_csv(csv_data, output_file_path)
print(f"Data has been written to {output_file_path}")

