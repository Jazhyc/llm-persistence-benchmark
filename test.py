import json


# load dataset/persistence.json and count number of entries
def count_entries():
    with open('dataset/persistence.json', 'r') as file:
        data = json.load(file)
        
    print("Number of entries: ", len(data))
    
if __name__ == "__main__":
    count_entries()