import numpy as np
import pandas as pd

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

import streamlit as st



#@st.cache(allow_output_mutation=True, hash_funcs={"builtins.function": extract_location})
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

#@st.cache(allow_output_mutation=True)
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

#@st.cache(allow_output_mutation=True)
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

#@st.cache(allow_output_mutation=True)
def create_location(df):

    df_dict = df.to_dict("records")

    dictionary_list = []
    for row in df_dict:
        ### creating list of location details

        # adding geo info
        dic = extract_location(row["text"])
        dic["region"] = dic["region"][0]
        dic["country"] = dic["country"][0]
        dic["city"] = dic["city"][0]

        # adding gps
        dic['lat'], dic['lon'] = extract_gps(dic['country'],dic['city'])
        dictionary_list.append(dic)

        # adding area size to the dictionary
        if dic['city'] == 'Unknown' and dic['country'] != 'Unknown':
            dic['size'] = get_area(dic['country'])
        else:
            dic['size'] = get_area(dic['city'])

        if dic['city'] != 'Unknown' and dic['country'] != 'Unknown' and dic['size'] == 'NotFound':
            dic['size'] = get_area(dic['country'])

        dictionary_list.append(dic)


    locations_df = pd.DataFrame.from_dict(data=dictionary_list)

    return locations_df
