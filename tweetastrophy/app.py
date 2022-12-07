import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
from location import create_location
from map import create_map
from predict import get_prediction


text_archive = []

# frontend style descriptors
hide_menu = """
<style>
#MainMenu {
    visibility:hidden;
}
footer {
    visibility:hidden;
}
</style>
"""
st.set_page_config(page_title='Tweetastrophy', page_icon=':tada:', layout='wide')

a, b = st.columns([1, 20])

with a:
    st.text("")
    st.image("tweetastrophy/twitter_logo.png", width=50)
with b:
    st.title("Tweetastrophy")

c, d = st.columns([500, 400])

with c:
    txt = st.text_area('Enter your tweet here 👇🏼', '')
    st.button('Predict')

# creating prediction value
prediction = get_prediction(txt)

with d:
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('', prediction)


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(hide_menu, unsafe_allow_html=True)

local_css("tweetastrophy/config.toml")


# creating text archive of all the txts
text_archive.append(txt)

text_archive = list(set(text_archive))

text_df = pd.DataFrame.from_dict(data={"text": text_archive})

locations_df = create_location(text_df)
# adding map based on the previous texts the person has entered
st_data = create_map(text_archive=text_archive, prediction=prediction, locations_df=locations_df)

# render Folium map in Streamlit
# st_data = st_folium(map, width=2000, height=600)
