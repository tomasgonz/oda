import colorsys
from re import S
import os
from this import d
from webbrowser import get
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.graph_objects as go
import random
from paises import Countries
from paises import Groups
from paises.alias import get_alias
import urllib
import importlib
from data import get_oda_recipients

st.set_page_config(layout="wide")

data = get_oda_recipients()

data = data[data['Year'] >= 1990]

data_2020 = data[data['Year'] == 2020].groupby(['Donor', 'Recipient'], as_index = False).sum()
data_2020.sort_values(by=['Value'], inplace=True, ascending=False)

years = data['Year'].unique()
series = data['Series'].unique()
recipients = data['Recipient'].unique()

data = data[data['Donor'] == 'Official Donors, Total']
selected_series = st.sidebar.selectbox('Select series', series)
if selected_series:
    data = data[data['Series'] == selected_series]

selected_recipient = st.sidebar.selectbox('Select recipient', recipients)
if selected_recipient != "all recipients":
    data = data[data['Recipient'] == selected_recipient]

# ODA evolution
st.header("An overview of the distribution of aid of aid to " + selected_recipient + " in the period 2000-2019")
    
st.write("The chart below represets " + selected_series +
    " to " + selected_recipient)

g = Groups()

fig_yearly = go.Figure()

def get_trace(data, name):
    return go.Scatter(x=data['Year'], y=data['Value'], name=name, fill='tozeroy')

fig_yearly.add_trace(get_trace(data[data['Recipient'] == selected_recipient], selected_recipient))

fig_yearly.update_layout(title='ODA to Developing Countries', xaxis_title='Year', 
    yaxis_title='ODA (USD)', height=600)

st.plotly_chart(fig_yearly, use_container_width=True)

# 2020
labels = data['Recipient'].unique().tolist()

if selected_recipient == 'all recipients':
    st.stop()

st.caption("""Beta ODA explorer development by Tomas Gonzalez using data from the OECD at https://stats.oecd.org/. 

This app is based on Streamlit and the source code is available at https://github.com/tomasgonz/oda. The source code is free to use, modify and distribute.""")

st.title("Aid (ODA) by sector and donor")

st.write(""" Official Development Assistance (ODA) is defined as those flows to developing countries and multilateral institutions provided by official agencies, including state and local governments, or by their executive agencies, each transaction of which meets the following tests: i) it is administered with the promotion of the economic development and welfare of developing countries as its main objective; and ii) it is concessional in character and conveys a grant element of at least 25 per cent. The data is in millions, current US. 

OECD (2022), "Data warehouse", OECD.Stat (database), https://doi.org/10.1787/data-00900-en (accessed on 12 October 2022). """
)

# 2020 - Recipients
# Data LDCs we get here before we filter for the selected recipient
ldcs = g.get_group('LDCs')
ldcs_and_aliases = get_alias(ldcs['names'])

data_ldcs = data_2020[data_2020['Recipient'].isin(ldcs_and_aliases)]

data_2020 = data_2020[data_2020['Recipient'] == selected_recipient]
data_2020 = data_2020[~data_2020['Donor'].str.contains('Official Donors')]

labels = data_2020['Donor'].unique().tolist() + recipients.tolist()

index_source = []
for e in data_2020['Donor'].values.tolist():
    index_source.append(labels.index(e))

index_destination = []
for e in data_2020['Recipient'].values.tolist():
    index_destination.append(labels.index(e))

st.header("How is aid being allocated to " + selected_recipient + " in 2020?")
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

fig.update_layout(height=1000)

st.plotly_chart(fig, font_size=10, use_container_width=True, height=1000)

if selected_recipient in ldcs_and_aliases:

    st.write(selected_recipient + " is part of the following political and economic groups ")

    ldc_sum = data_ldcs['Value'].sum()

    selected_sum = data_ldcs[data_ldcs['Recipient'] == selected_recipient]['Value'].sum()

    st.write(selected_recipient + " represents " + str((selected_sum / ldc_sum).round(2)*100) +  " per cent of " + selected_series + " for the LDCs")