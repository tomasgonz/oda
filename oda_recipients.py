import colorsys
from re import S
import os
from webbrowser import get
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.graph_objects as go
import random
from paises import Countries
from paises import Groups
import urllib
import importlib

st.set_page_config(layout="wide")


def check_if_file_exists(file_name):
    if os.path.isfile(file_name):
        st.write("File exists locally. No need to download it again.")
        return True
    else:
        download_file()
        return False

@st.cache(ttl=1*60*60)

def download_file():
    st.write("Downloading data. Please, be patient... it is a lot of data...")
    url = "https://datasource.nyc3.digitaloceanspaces.com/oecd_table2a_data.csv"
    
    urllib.request.urlretrieve(url, "oecd_table2a_data.csv")

check_if_file_exists("oecd_table2a_data.csv")

data = pd.DataFrame()

data = pd.read_csv(os.path.join(os.path.dirname(__file__), "oecd_table2a_data.csv"), encoding = "ISO-8859-1")

donors = data['Donor'].unique()
years = data['Year'].unique()
aid_types = data['Aid type'].unique()

data = data[~data['Recipient'].str.contains('Total')]
data = data[~data['Recipient'].str.contains('regional')]
data = data[~data['Recipient'].str.contains('WorldBank')]
data = data[~data['Recipient'].str.contains('World Bank')]

recipients = data['Recipient'].unique()

data = data[data['Aid type'] == 'ODA: Total Net']
data = data[data['Amount type'] == 'Current Prices (USD millions)']
data = data[data['Year'] == 2020]

selected_donor = st.sidebar.selectbox('Select a donor', donors)
if selected_donor != "all donors":
        data = data[data['Donor'] == selected_donor]

selected_recipient = st.sidebar.selectbox('Select a recipient', recipients)
if selected_recipient:
    if selected_recipient != "all recipients":
        data = data[data['Recipient'] == selected_recipient]


st.sidebar.write(data.columns)
st.sidebar.write(aid_types)
st.sidebar.write(years)

st.metric("Total Net ODA: 2020", data['Value'].sum())

st.write(data)