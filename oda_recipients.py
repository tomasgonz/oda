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
    df =  pd.read_csv(os.path.join(os.path.dirname(__file__), "data/DACGEO_Data.csv"), encoding = "ISO-8859-1")
    return df

data = load_data()

data = data[data['Year'] >= 2000]

donors = data['Donor'].unique()
years = data['Year'].unique()
series = data['Series'].unique()
recipients = data['Recipient'].unique()
recipients = np.insert(recipients, 0, "all recipients")

#data = data[~data['Recipient'].str.contains('Total')]
#data = data[~data['Recipient'].str.contains('regional')]
#data = data[~data['Recipient'].str.contains('WorldBank')]
#data = data[~data['Recipient'].str.contains('World Bank')]
#data = data[~data['Recipient'].str.contains('World Bank')]
#data = data[~data['Recipient'].str.contains('Part')]

selected_donor = st.sidebar.selectbox('Select a donor', donors)
if selected_donor != "all donors":
        data = data[data['Donor'] == selected_donor]

selected_recipient = st.sidebar.selectbox('Select a recipient', recipients)
if selected_recipient:
    if selected_recipient != "all recipients":
        data = data[data['Recipient'] == selected_recipient]

selected_series = st.sidebar.selectbox('Select series', series)
if selected_series:
    data = data[data['Series'] == selected_series]

# ODA evolution
st.header("An overview of the distribution of aid of " + selected_donor)

st.write("The chart below represets " + selected_series +
     " from " + selected_donor + " various groups of developing countries as reported to the DAC. The data is extracted from the DAC Geobook.")

fig_yearly = go.Figure()

def get_trace(data, name):
    return go.Scatter(x=data['Year'], y=data['Value'], name=name, fill='tozeroy')

fig_yearly.add_trace(get_trace(data[data['Recipient'] == 'Developing Countries, Total'], 
    'Developing Countries, Total'))
fig_yearly.add_trace(get_trace(data[data['Recipient'] == 'LDCs, Total'], 'LDCs, Total'))
fig_yearly.add_trace(get_trace(data[data['Recipient'] == 'Africa, Total'], 'Africa, Total'))
fig_yearly.add_trace(get_trace(data[data['Recipient'] == 'Asia, Total'], 'Asia, Total'))
fig_yearly.add_trace(get_trace(data[data['Recipient'] == 'LMICs, Total'], 'LMICs, Total'))
fig_yearly.add_trace(get_trace(data[data['Recipient'] == 'UMICs, Total'], 'UMICs, Total'))
fig_yearly.add_trace(get_trace(data[data['Recipient'] == 'Europe, Total'], 'Europe, Total'))
fig_yearly.add_trace(get_trace(data[data['Recipient'] == 'Middle East, Total'], 'Middle East, Total'))
fig_yearly.add_trace(get_trace(data[data['Recipient'] == 'America, Total'], 'America, Total'))


fig_yearly.update_layout(title='ODA to Developing Countries', xaxis_title='Year', 
    yaxis_title='ODA (USD)', height=600)

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

fig = go.Figure(data=[go.Treemap(
    labels=labels,
    parents= index_destination,
    values=data_2020['Value'].values.tolist(),
    branchvalues="total",
    marker=dict(
        colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'] * 2,
        line=dict(width=2, color='#000000')
    ),
    textinfo='label+value',
    hovertemplate = '%{label}<extra></extra>',
    pathbar=dict(visible=False),
    maxdepth=2
)])

fig.update_layout(height=1500)

st.plotly_chart(fig, font_size=10, use_container_width=True, height=2000)

st.header("How have the trends of recipients of aid by " + selected_donor + " to " + selected_recipient + " evolved from 2010 to 2020?")