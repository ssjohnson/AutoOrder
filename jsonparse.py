import json

with open('items.json') as data_file:
    data = json.load(data_file)

def getParts():
    return data['Parts']