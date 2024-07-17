import json

def read_saved_ids(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data.get("saved_ids", [])
    except FileNotFoundError:
        return []

def write_saved_ids(filename, saved_ids):
    with open(filename, 'w') as file:
        json.dump({"saved_ids": saved_ids}, file, indent=4)
