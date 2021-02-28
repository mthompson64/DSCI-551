from bs4 import BeautifulSoup
import random
import requests
import re
import csv

# Select a random user agent
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

def get_zip_data(state, filename):
    # Input two-digit state code only
    if len(state) > 2:
        print('Enter two-digit state code only')
    state = state.lower()
    main_url = "https://www.zip-codes.com"
    append_url = f"/state/{state}.asp"
    # Access URL using one of the randomly chosen user agents
    page = requests.get(
        main_url + append_url,
        headers = {'User-Agent': select_user()}
    )
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table', {'class': 'statTable'})
    indices = table.find_all('tr')
    for row in indices:
        if row.find('a'):
            table_data = row.find_all('td')
            # Check that ZIP code is not a P.O. Box and continue
            if table_data[-1].string.lower() == "standard":
                zip_id = row.find('a', {'title': re.compile("ZIP Code ")})
                zip_code = int(zip_id.string.split()[-1])
                zip_url = main_url + zip_id.get('href')
                # Go to the URL specific to that ZIP code to check for latitude, longitude, and population data
                zc = requests.get(
                    zip_url,
                    headers = {'User-Agent': select_user()}
                )
                zsoup = BeautifulSoup(zc.content, 'html.parser')
                tables = zsoup.find_all('table', {'class': 'statTable'})
                for table in tables:
                    for data in table.find_all('td'):
                        if str(data.string).lower() == 'latitude:':
                            latitude = float(data.next_sibling.string)
                        if str(data.string).lower() == 'longitude:':
                            longitude = float(data.next_sibling.string)
                        if str(data.string).lower() == 'current population:':
                            population = int(data.next_sibling.string.replace(",",""))
                        if str(data.string).lower() == 'average house value:':
                            house_value = int(data.next_sibling.string.replace("$","").replace(",",""))
                        if str(data.string).lower() == 'avg. income per household:':
                            household_income = int(data.next_sibling.string.replace("$","").replace(",",""))
                try:
                    filename.writerow([state.upper(), zip_code, zip_url, latitude, longitude, population, house_value, household_income])
                except:
                    print(f"Issue appending data for {zip_code}")
        zip_code = None
        zip_url = ''
        latitude = None
        longitude = None
        longitude = None
        population = None

with open('zip_codes.csv', 'w') as new_file:
    f = csv.writer(new_file)
    f.writerow(['state', 'zip_code', 'zip_url', 'latitude', 'longitude', 'population', 'house_value', 'household_income'])
    get_zip_data('DC', f)
    print("All zip codes retrieved for DC")
    new_file.close()

with open('zip_codes.csv', 'a') as new_file:
    f = csv.writer(new_file)
    get_zip_data('VA', f)
    print("All zip codes retrieved for VA")
    get_zip_data('MD', f)
    print("All zip codes retrieved for MD")
    new_file.close()
    print("Done")