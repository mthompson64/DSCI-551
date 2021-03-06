import urllib.request, urllib.parse, urllib.error
import json
import pandas as pd
import random
import requests
import csv

# Choose a random user agent
def select_user():
    user_agents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',	
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.0; rv:83.0) Gecko/20100101 Firefox/83.0',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/29.0 Mobile/15E148 Safari/605.1.15',
        'Mozilla/5.0 (iPad; CPU OS 11_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/29.0 Mobile/15E148 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
    ]
    return random.choice(user_agents)

def get_commute(ZIP, latitude, longitude):
    params = {
        'origins': "%.4f,%.4f" % (latitude, longitude),
        # Destination is the Pentagon, coordinates are 38.8719° N, 77.0563° W
        'destinations': '38.8719,-77.0563',
        'units': 'imperial',
        'key': 'API-key'
    }
    serviceurl = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
    url = serviceurl + urllib.parse.urlencode(params)
    response = requests.get(
        url,
        headers = {'User-Agent': select_user()}
    )
    try:
        resp_json = response.json()
        distance = resp_json['rows'][0]['elements'][0]['distance']['text']
        duration = resp_json['rows'][0]['elements'][0]['duration']['text']
    except:
        distance = None
        duration = None
    return distance, duration


df = pd.read_csv('/Users/madeleine/Desktop/DSCI_551/Project/Data/zip_codes.csv')
with open('commute_info.csv', 'w') as new_file:
    f = csv.writer(new_file)
    f.writerow(['zip_code', 'latitude', 'longitude', 'distance', 'duration'])
    for index in df.index:
        zip_code = df.loc[index, 'zip_code']
        latitude = df.loc[index, 'latitude']
        longitude = df.loc[index, 'longitude']
        dist, dur = get_commute(zip_code, latitude, longitude)
        print(f"{zip_code}: {latitude}, {longitude} - {dist} {dur}")
        f.writerow([zip_code, latitude, longitude, dist, dur])
        print("Updated successfully!")
    new_file.close()
