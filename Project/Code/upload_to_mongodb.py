import csv
import json
from pymongo import MongoClient
 
# Function to convert a CSV to JSON
# Takes the file paths as arguments
def make_json(csvFilePath, jsonFilePath):
     
    # create a dictionary
    data = []
     
    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
         
        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:
            
            data.append(rows)
 
    # Open a json writer, and use the json.dumps()
    # function to dump data
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonOut:
        json.dump(data, jsonOut, indent=4)

def change_json(originaljson, newjson):
    
    data = []

    with open(originaljson, encoding='utf-8') as jsonf:
        old_data = json.load(jsonf)
    
    for key, value in old_data.items():
        for i in value:
            data.append(i)

    with open(newjson, 'w', encoding='utf-8') as jsonOut:
        json.dump(data, jsonOut, indent=4)

def upload(jsonFile):
    mongo_client = MongoClient()
    db = mongo_client.project
    col = db.restaurants
    with open(jsonFile, 'r', encoding='utf-8') as jsonf:
        data = json.load(jsonf)
    col.insert_many(data)


# Driver Code
 
# Call the make_json function

#make_json('/Users/madeleine/Desktop/DSCI_551/Project/Data/zip_codes.csv', '/Users/madeleine/Desktop/DSCI_551/Project/Data/zip_codes.json')

#make_json('/Users/madeleine/Desktop/DSCI_551/Project/Data/commute_info.csv', '/Users/madeleine/Desktop/DSCI_551/Project/Data/commute_info.json')

#change_json('/Users/madeleine/Desktop/DSCI_551/Project/Data/restaurant_data.json', '/Users/madeleine/Desktop/DSCI_551/Project/Data/restaurant_data_2.json')

upload('/Users/madeleine/Desktop/DSCI_551/Project/Data/restaurant_data.json')