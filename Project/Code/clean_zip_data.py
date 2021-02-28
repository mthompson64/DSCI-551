from bs4 import BeautifulSoup
import random
import requests
import pandas as pd
import numpy as np

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

def get_url(url):
    page = requests.get(
        url,
        headers = {'User-Agent': select_user()}
    )
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def clean_data(filename):
    df = pd.read_csv(filename)
    for index in df.index:
        if df.loc[index, 'population'] == 0:
            df.drop(index, inplace=True)
        if np.isnan(df.loc[index, 'latitude']):
            soup = get_url(df.loc[index, 'zip_url'])
            for table in soup.find_all('table'):
                cols = table.find_all('td')
                for data in cols:
                    if str(data.string).lower() == 'latitude:':
                        df.at[index, 'latitude'] = float(data.next_sibling.string)
                    if str(data.string).lower() == 'longitude:':
                        df.at[index, 'longitude'] = float(data.next_sibling.string)
    df.to_csv('zip_codes_copy.csv', index=False)
    print('Done')
clean_data('zip_codes.csv')