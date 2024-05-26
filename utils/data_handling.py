import csv
import json

class FileHandler:
    
    def __init__(self, dataset_name):
        self.dataset_name = dataset_name

    # Load data from json
    def load_data(self):
        with open(f'datasets/{self.dataset_name}.json', 'r') as file:
            data = json.load(file)
            
        return data
        
    
    # Convert lists of dicts to json and save to file
    def save_data(self, data):
        with open(f'outputs/{self.dataset_name}.json', 'w') as file:
            json.dump(data, file)