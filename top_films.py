from bs4 import BeautifulSoup
import requests
import re
import time
from utils import db_params, insert_f, select_f
import logging

ts = time.time()

url = 'https://www.cinemarealm.com/best-of-cinema/empires-500-greatest-movies-of-all-time/'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
raw_content = str(soup.find('div', class_='entry-content'))

pattern = r'<strong>(.*)</strong>.*\((.*),.*(\d{4})\)\<'
extracted = re.findall(pattern, raw_content)

# insert dato into db
insert_f(extracted, 'top500_films')

query_get_films = '''SELECT title, year FROM top500_films'''
films_from_db = select_f(query_get_films)


api_url = 'http://www.omdbapi.com'
api_key = '5cc4eea8'
tags = [
    "Title",
	"Year",
	"Rated",
	"Runtime",
	"Genre",
	"Director",
	"Actors",
	"Plot",
	"Country",
	"Awards",
	"Poster",
	"imdbRating",
	"imdbVotes",
    'BoxOffice',
    'imdbID'
]

film_details = []

for film in films_from_db:
    params = {
        'apikey' : api_key,
        't' : film[0],
        'y' : str(film[1])
    }
    try:
        response = requests.get(api_url, params=params)
        api_data = response.json()

        # if fail, then skip
        if api_data.get('Response') == 'False':
            print(api_data.get('Error'), film)
            continue
        
        # unpacking film details in correct order
        film_details.append(tuple(api_data.get(tag) for tag in tags))

    # log errors
    except Exception as e:
        logging.error(traceback.format_exc())

# insert details into db
insert_f(film_details, 'films_data')

te = time.time()

print(te-ts)
