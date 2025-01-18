import streamlit as st
import pandas as pd
import requests
import json

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
    census_df = pd.DataFrame(census_data_json).transpose()
    census_df.columns = ["variable", "value"]
    variable_to_name_lookups = get_census_variable_mapping()
    census_df['display_name'] = census_df['variable'].map(variable_to_name_lookups)
    return census_df

def get_census_meta_data():
    url = "https://api.census.gov/data/2023/acs/acs1/subject"
    census_meta_data_resp = requests.get(url)
    census_meta_data_json = census_meta_data_resp.json()
    return census_meta_data_json["dataset"][0]["description"]

@st.cache_data
def get_census_variable_mapping():
    with open("data/acs-acs1-subject-groups-s2901.json", "r") as f:
        content = json.loads(f.read())
    
    mapping = {}
    for element in content:
        mapping[element["variable"]] = element["calc_info"]
    return mapping
    # url = "https://api.census.gov/data/2023/acs/acs1/subject/groups/S2901.html"
    # census_meta_data_resp = requests.get(url)
    # html_string = census_meta_data_resp.text
    # output_json = html_to_json.convert(html_string)
    # return output_json

st.text(get_census_meta_data())
st.table(get_census_data())
