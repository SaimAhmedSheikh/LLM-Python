from utils import  read_data

test_results = read_data('test_results.json')
explanations = read_data('explanations.json')

data = []
combined = {}

for i in range(0, len(test_results)):
    test = test_results[i]
    patient_data = test['patient_data']