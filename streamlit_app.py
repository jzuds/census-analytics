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

# Powered by [Census Bureau Data](https://data.census.gov) website.
# '''
