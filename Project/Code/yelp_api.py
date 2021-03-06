import urllib.request, urllib.parse, urllib.error
import json
import pprint
import pandas as pd
import random
import requests

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

def get_restaurants(ZIP, jsons):
    api_key = 'NlKocY3aC47E_KzOHymO-cp9t5FQRBgAhPkj5oBUGKoCvSUPH6riKuwBH-QhUbVZcNrpVwwwA7k4Vb2as1Yz7bKZMJJsRLIWmt5ZyRUi8dXqc1sccoh1VVeymT29X3Yx'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'User-Agent': select_user()
    }
    params = { 
        'term': 'restaurant',
        'location': ZIP,
        'categories': 'vegan,vegetarian,cafes'
    }
    # The API requires that I authenticate with the 'Authorization' field in the header set to 'Bearer API_KEY'
    serviceurl = 'https://api.yelp.com/v3/businesses/search?'
    url = serviceurl + urllib.parse.urlencode(params)
    response = requests.get(
        url,
        headers = headers
    )
    # The data I want is stored in the 'businesses' key as a list of businesses
    try:
        data = response.json()['businesses']
    except:
        data = []
    restaurants = []
    for item in data:
        # If the ZIP code is empty, skip
        if item['location']['zip_code'] == '' or item['location']['zip_code'] is None:
            continue
        # Check that the ZIP code is equal to the ZIP code passed into the function. Otherwise, skip.
        elif int(item['location']['zip_code']) == ZIP:
            # Identify each of the items I want to keep and append to my database
            name = item['name']
            restaurant_id = item['id']
            address1 = item['location']['address1']
            address2 = item['location']['address2']
            # Include the second address line if it has it
            address = "{Line1}{Line2}".format(Line1=address1, Line2=" "+ address2 if address2 is not None else "")
            city = item['location']['city']
            zip_code = int(item['location']['zip_code'])
            restaurants.append({'restaurant_id': restaurant_id, 'ZIP_code': zip_code, 'restaurant_name': name, 'address': address, 'city': city})
    if len(restaurants) > 0:
        jsons[str(ZIP)] = restaurants
    return jsons  

def main():
    df = pd.read_csv('/Users/madeleine/Desktop/DSCI_551/Project/Data/zip_codes.csv')
    jsons = {}
    for index in df.index:
        zip_code = df.loc[index, 'zip_code']
        try:
            jsons = get_restaurants(zip_code, jsons)
            print(f"{zip_code} successfully appended!")
        except:
            print(f"{zip_code} ERROR APPENDING")
            continue
    with open('restaurant_data.json', 'w') as outfile:
        json.dump(jsons, outfile)
        outfile.close()
    # Somehow add all the restaurants to a csv file (maybe make a pandas dataframe out of them?)
    print("All done!")

if __name__ == '__main__':
    main()