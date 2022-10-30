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

@st.cache(ttl=1*60*60)
def load_data():
    df =  pd.read_csv(os.path.join(os.path.dirname(__file__), "oecd_table2a_data.csv"), encoding = "ISO-8859-1")
    return df

data = load_data()

data = data[data['Year'] >= 2000]

donors = data['Donor'].unique()
years = data['Year'].unique()
aid_types = data['Aid type'].unique()

all_recipients = recipients = data['Recipient'].unique()

data = data[~data['Recipient'].str.contains('Total')]
data = data[~data['Recipient'].str.contains('regional')]
data = data[~data['Recipient'].str.contains('WorldBank')]
data = data[~data['Recipient'].str.contains('World Bank')]
data = data[~data['Recipient'].str.contains('World Bank')]
data = data[~data['Recipient'].str.contains('Part')]

recipients = data['Recipient'].unique()
recipients = np.insert(recipients, 0, "all recipients")

st.sidebar.write(recipients)

selected_donor = st.sidebar.selectbox('Select a donor', donors)
if selected_donor != "all donors":
        data = data[data['Donor'] == selected_donor]

selected_recipient = st.sidebar.selectbox('Select a recipient', recipients)
if selected_recipient:
    if selected_recipient != "all recipients":
        data = data[data['Recipient'] == selected_recipient]

selected_aid_type = st.sidebar.selectbox('Select am aid type', aid_types)
if selected_aid_type:
    data = data[data['Aid type'] == selected_aid_type]

# ODA evolution

data_yearly = data.groupby(['Year'])['Value'].sum().reset_index()

fig_yearly = go.Figure(data=go.Scatter(x=data_yearly['Year'], y=data_yearly['Value'], mode='lines+markers'))
fig_yearly.update_layout(title='ODA evolution', xaxis_title='Year', yaxis_title='ODA (USD)')
st.plotly_chart(fig_yearly, use_container_width=True)


# 2020
data_2020 = data[data['Year'] == 2020].groupby(['Donor', 'Recipient'], as_index = False).sum()

labels =  data_2020['Donor'].unique().tolist() + recipients.tolist()

index_source = []
for e in data_2020['Donor'].values.tolist():
    index_source.append(labels.index(e))

index_destination = []
for e in data_2020['Recipient'].values.tolist():
    index_destination.append(labels.index(e))

st.header("How is " + selected_donor + " allocating its aid to " + selected_recipient + " by sector in 2020?")
st.write("The size of the arrows represents the amount of aid allocated to each recipient. The color of the arrows represents the sector of the aid. The size of the nodes represents the total amount of aid received by each recipient. The color of the nodes represents the region of the recipient.")

fig = go.Figure(data=[go.Sankey(
    node = {
        'pad' : 15,
        'thickness' : 20,
        'line' : {
            'color' : 'black', 
            'width' : 0.5
        },
        'label' :labels
    },
    link = {
        'source' : index_source,
        'target' : index_destination,
        'value' : data_2020['Value']
    }
)])

fig.update_layout(height=1500)
st.plotly_chart(fig, font_size=10, use_container_width=True, height=2000)

st.header("How have the trends of recipients of aid by " + selected_donor + " to " + selected_recipient + " evolved from 2010 to 2020?")