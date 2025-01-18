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
    census_df.columns = ["Variable", "Value"]
    variable_to_name_lookups = get_census_variable_mapping()
    census_df['display_name'] = census_df['Variable'].map(variable_to_name_lookups)
    #census_df["display_name"].str.split('!!', n=0, expand=False)
    column_info = pd.Series(census_df["display_name"].str.split('!!', n=None, expand=False), index=census_df.index)
    census_df["Name"] = column_info.str[0]
    census_df["Type"] = column_info.str[1]
    census_df["Demographic"] = column_info.str[2]
    census_df.drop("display_name", axis=1, inplace=True)

    # Reordering columns using loc
    census_df = census_df.loc[:, ['Variable', 'Name', 'Type', 'Demographic', 'Value']]
    return census_df

@st.cache_data
def get_census_meta_data():
    url = "https://api.census.gov/data/2023/acs/acs1/subject"
    census_meta_data_resp = requests.get(url)
    census_meta_data_json = census_meta_data_resp.json()
    return census_meta_data_json["dataset"][0]["description"]

@st.cache_data
def get_census_variable_mapping():
    # url = "https://api.census.gov/data/2023/acs/acs1/subject/groups/S2901" TODO: use this mapping instead of static
    with open("data/acs-acs1-subject-groups-s2901.json", "r") as f:
        content = json.loads(f.read())
    
    mapping = {}
    for element in content:
        mapping[element["variable"]] = element["calc_info"]
    return mapping

def render_dropdown(name: str, dropdown_options:pd.DataFrame):
    st.selectbox(label=name, options=dropdown_options)

##################################################
## Main
##################################################

data = get_census_data()
st.text(get_census_meta_data())
st.table(data)
