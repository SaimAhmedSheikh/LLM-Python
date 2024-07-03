from utils import  read_data, write_data_to_file, write_data_to_csv

test_results = read_data('result_data.json')


results = []
for i in range(0, len(test_results)):
    test_result = test_results[i]
    results.extend(test_result['result']['results'])

output_file_path = "results.json"
write_data_to_file(results, output_file_path)
print(f"Data has been written to {output_file_path}")
print(f"Number of files: {len(results)}")

output_file_path = "results.csv"
write_data_to_csv(results, output_file_path)
print(f"Data has been written to {output_file_path}")
