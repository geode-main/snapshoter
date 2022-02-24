import json
from os import listdir
import csv


def collectTokensData(dataPath):
    data = {}
    dataFiles = [f for f in listdir(dataPath)]
    for file in dataFiles:
        with open(dataPath + file) as data_json:
            data[file.split('.', 1)[0]] = json.load(data_json)
    return data


def saveResults(data, name):
    with open(f'./results/{name}.json', 'w') as f:
        json.dump(data, f)
    with open(f'./results/{name}.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(["Address", "Balance"])
        # write the data
        for key, value in data.items():
            writer.writerow([key, value])
