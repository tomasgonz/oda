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
import urllib
import importlib
from data import get_oda_recipients

st.set_page_config(layout="wide")

data = get_oda_recipients()

data = data[data['Year'] >= 2000]

donors = data['Donor'].unique()
years = data['Year'].unique()
series = data['Series'].unique()
recipients = data['Recipient'].unique()

data_selected_donor = data

selected_donor = st.sidebar.selectbox('Select a donor', donors)
if selected_donor != "all donors":
        data_selected_donor = data_selected_donor[data_selected_donor['Donor'] == selected_donor]

selected_series = st.sidebar.selectbox('Select series', series)
if selected_series:
    data_selected_donor = data_selected_donor[data_selected_donor['Series'] == selected_series]

recipients =  np.insert(recipients, 0, "all recipients")

selected_recipient = st.sidebar.selectbox('Select recipient', recipients)
if selected_recipient != "all recipients":
    data_selected_donor = data_selected_donor[data_selected_donor['Recipient'] == selected_recipient]

st.sidebar.caption("""Beta ODA explorer development by Tomas Gonzalez using data from the OECD at https://stats.oecd.org/. 

This app is based on Streamlit and the source code is available at https://github.com/tomasgonz/oda. The source code is free to use, modify and distribute.""")

# ODA evolution
st.header("An overview of the distribution of aid")

st.write("""Distribution of net official development assistance (ODA) is defined as geographical aid allocations. 
Net ODA may be distributed by income group (least developed countries, other low-income countries, lower middle-income countries, upper middle-income countries, unallocated and more advanced developing countries and territories) or by geography (sub-Saharan Africa, South and Central Asia, other Asia and Oceania, Middle East and North Africa, Latin America and the Caribbean, Europe, and unspecified). The OECD Development Assistance Committee's "List of ODA Recipients" shows developing countries and territories eligible for ODA. The list is revised every three years. It is designed for statistical purposes, not as guidance for aid distribution or for other preferential treatment. 
In particular, geographical aid allocations are national policy decisions and responsibilities.""")

st.write("The chart below represets '" + selected_series +
     "' from '" + selected_donor + "' various groups of developing countries as reported to the DAC. The data is extracted from the DAC Geobook.")

fig_yearly = go.Figure()

def get_trace(data_selected_donor, name):
    return go.Scatter(x=data_selected_donor['Year'], y=data_selected_donor['Value'], name=name, fill='tozeroy')

fig_yearly.add_trace(get_trace(data_selected_donor[data_selected_donor['Recipient'] == 'Developing Countries, Total'], 
    'Developing Countries, Total'))
fig_yearly.add_trace(get_trace(data_selected_donor[data_selected_donor['Recipient'] == 'LDCs, Total'], 'LDCs, Total'))
fig_yearly.add_trace(get_trace(data_selected_donor[data_selected_donor['Recipient'] == 'Africa, Total'], 'Africa, Total'))
fig_yearly.add_trace(get_trace(data_selected_donor[data_selected_donor['Recipient'] == 'Asia, Total'], 'Asia, Total'))
fig_yearly.add_trace(get_trace(data_selected_donor[data_selected_donor['Recipient'] == 'LMICs, Total'], 'LMICs, Total'))
fig_yearly.add_trace(get_trace(data_selected_donor[data_selected_donor['Recipient'] == 'UMICs, Total'], 'UMICs, Total'))
fig_yearly.add_trace(get_trace(data_selected_donor[data_selected_donor['Recipient'] == 'Europe, Total'], 'Europe, Total'))
fig_yearly.add_trace(get_trace(data_selected_donor[data_selected_donor['Recipient'] == 'Middle East, Total'], 'Middle East, Total'))
fig_yearly.add_trace(get_trace(data_selected_donor[data_selected_donor['Recipient'] == 'America, Total'], 'America, Total'))

if selected_recipient:
    fig_yearly.add_trace(get_trace(data_selected_donor[data_selected_donor['Recipient'] == selected_recipient], selected_recipient))

st.header("Aggregate aid to developing countries")

fig_yearly.update_layout(title='ODA to Developing Countries', xaxis_title='Year', 
    yaxis_title='ODA (USD)', height=600)

st.plotly_chart(fig_yearly, use_container_width=True)

# 2020
data_2020 = data[data['Year'] == 2020].groupby(['Donor', 'Recipient'], as_index = False).sum()
data_2020.sort_values(by=['Value'], inplace=True, ascending=False)

labels = data['Recipient'].unique().tolist()

parents = [selected_donor] * len(labels)

st.header("How is " + selected_donor + " allocating its aid by country or region?")
st.write("The size of the arrows represents the amount of aid allocated to each recipient. The color of the arrows represents the sector of the aid. The size of the nodes represents the total amount of aid received by each recipient. The color of the nodes represents the region of the recipient.")

fig = go.Figure(data=[go.Treemap(
    labels=labels,
    parents=parents,
    values=data['Value']
)])

fig.update_layout(height=800)

st.plotly_chart(fig, font_size=10, use_container_width=True, height=2000)

st.header("How is " + selected_donor + " allocating its aid by country?")
st.write("The same as above, but excluding country group aggregates and showing only individual countries. Note that for some countries a substantial volume of aid is reported as unspecified.")

data = data[~data['Recipient'].str.contains('Total')]
data = data[~data['Recipient'].str.contains('regional')]
data = data[~data['Recipient'].str.contains('WorldBank')]
data = data[~data['Recipient'].str.contains('World Bank')]
data = data[~data['Recipient'].str.contains('World Bank')]
data = data[~data['Recipient'].str.contains('Part')]
data = data[~data['Recipient'].str.contains('unspecified')]

data_2020.sort_values(by=['Value'], inplace=True, ascending=False)

labels = data['Recipient'].unique().tolist()

parents = [selected_donor] * len(labels)

fig = go.Figure(data=[go.Treemap(
    labels=labels,
    parents=parents,
    values=data['Value']
)])

fig.update_layout(height=800)

st.plotly_chart(fig, font_size=10, use_container_width=True, height=2000)

if selected_recipient == 'all recipients':
    st.stop()

st.caption("""Beta ODA explorer development by Tomas Gonzalez using data from the OECD at https://stats.oecd.org/. 

This app is based on Streamlit and the source code is available at https://github.com/tomasgonz/oda. The source code is free to use, modify and distribute.""")

st.title("Aid (ODA) by sector and donor")

st.write(""" Official Development Assistance (ODA) is defined as those flows to developing countries and multilateral institutions provided by official agencies, including state and local governments, or by their executive agencies, each transaction of which meets the following tests: i) it is administered with the promotion of the economic development and welfare of developing countries as its main objective; and ii) it is concessional in character and conveys a grant element of at least 25 per cent. The data is in millions, current US. 

OECD (2022), "Data warehouse", OECD.Stat (database), https://doi.org/10.1787/data-00900-en (accessed on 12 October 2022). """
)

# 2020 - Recipients

data_2020 = data[data['Year'] == 2020].groupby(['Donor', 'Recipient', 'Year'], as_index = False)['Value'].sum()

data_2020 = data_2020[data_2020['Recipient'] == selected_recipient]

data_2020 = data_2020[~data_2020['Donor'].str.contains('Official Donors')]

labels = data_2020['Donor'].unique().tolist() + recipients.tolist()

index_source = []
for e in data_2020['Donor'].values.tolist():
    index_source.append(labels.index(e))

index_destination = []
for e in data_2020['Recipient'].values.tolist():
    index_destination.append(labels.index(e))

st.header("How is " + selected_donor + " allocating its aid by recipient in 2020?")
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