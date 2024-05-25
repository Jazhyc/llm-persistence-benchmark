import csv
import json

class FileHandler:
    
    def __init__(self, dataset_name):
        self.dataset_name = dataset_name

    def load_data(self):
        with open(f'dataset/{self.dataset_name}.csv', 'r') as file:
            dict_reader = csv.DictReader(file)
            
            # Return a dictionary with the data
            return list(dict_reader)
    
    # Convert lists of dicts to json and save to file
    def save_data(self, data):
        with open(f'outputs/{self.dataset_name}.json', 'w') as file:
            json.dump(data, file)