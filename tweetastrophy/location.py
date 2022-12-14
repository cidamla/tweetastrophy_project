import numpy as np

import spacy
spacy.cli.download("en_core_web_sm")

import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

import locationtagger
from geopy.geocoders import Nominatim

from bs4 import BeautifulSoup
import requests
import string
import re




def extract_location(text):

    place_entity = locationtagger.find_locations(text = text)

    dic = {'region':place_entity.regions,
        'country':place_entity.countries,
        'city': place_entity.cities,
        'place': place_entity.other}
    if len(dic['country']) == 0:
        dic['country'] = [country for country in place_entity.country_cities.keys()]
        if len(dic['country']) == 0:
            dic['country'] = [country for country in place_entity.country_regions.keys()]


    for k in dic.keys():
        if len(dic[k]) == 0:
              dic[k] = ['Unknown']
    return dic

def extract_gps(country, city):

    loc  = Nominatim(user_agent="tweetastrophy")


    if city != 'Unknown':
        getLoc = loc.geocode(city, exactly_one=True, timeout=10)
        return getLoc.latitude, getLoc.longitude

    elif country != 'Unknown':
        getLoc = loc.geocode(country, exactly_one=True, timeout=10)
        return getLoc.latitude, getLoc.longitude
    else:
        return 0,0

def get_area(city):
    url = f"https://en.wikipedia.org/wiki/{city}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find('table', {'class': 'infobox'})
    try:
        for th in table:
            res = re.search('km' , th.text)
            if res != None:
                span = res.span()
                num = th.text[span[0]-15:span[1]]
                num = ''.join(digit for digit in num if digit in string.digits)
                return int(num)
            else:
                return 'NotFound'
    except:
        return 'NotFound'

def create_location(df):

    ls = ['region','country','city']
    for k in ls:
        df[k] = df['text'].apply(lambda x: extract_location(x)[k][0])

    df['lat'] = np.nan
    df['lon'] = np.nan
    df['size'] = np.nan
    for x, y in df.iterrows():
        df['lat'].iloc[x], df['lon'].iloc[x] = (extract_gps(y['country'],y['city']))
        if y['city'] == 'Unknown' and y['country'] != 'Unknown':
            df['size'].iloc[x] = get_area(y['country'])
        else:
            df['size'].iloc[x] = get_area(y['city'])

        if y['city'] != 'Unknown' and y['country'] != 'Unknown' and y['size'] != 'NotFound':
            df['size'].iloc[x] = get_area(y['country'])

    return df
