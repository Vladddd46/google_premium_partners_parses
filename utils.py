import json
import os

def save_json(filename, data):
	with open(filename, 'w') as file:
		json.dump(data, file, indent=4)

def read_json(filename):
	with open(filename, 'r') as file:
		data = json.load(file)
	return data

def file_exist(filename):
	return os.path.exists(filename)

	
