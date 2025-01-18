import streamlit as st
import pandas as pd
import requests
from pathlib import Path
import datetime

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    layout='centered',
    page_title='Census Analytics',
    page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
)

# Set the title that appears at the top of the page.
'''
# :earth_americas: Census Analytics

# Powered by data from the [Census Bureau Data](https://data.census.gov) website.
Author: Josh Zadoyko
# '''

def get_census_data():
    """
    https://api.census.gov/data/2023/acs/acs1/subject/groups/S2901.html
    """
    url = "https://api.census.gov/data/2023/acs/acs1/subject?get=group(S2901)&ucgid=0100000US"
    census_data_resp = requests.get(url)
    census_data_json = census_data_resp.json()
    return pd.DataFrame(census_data_json).transpose()

def get_census_meta_data():
    url = "https://api.census.gov/data/2023/acs/acs1/subject"
    census_meta_data_resp = requests.get(url)
    census_meta_data_json = census_meta_data_resp.json()
    return census_meta_data_json["dataset"][0]["description"]

st.text(get_census_meta_data())
st.table(get_census_data())
