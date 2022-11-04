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

data = data

selected_donor = st.sidebar.selectbox('Select a donor', donors)
if selected_donor != "all donors":
        data = data[data['Donor'] == selected_donor]

selected_series = st.sidebar.selectbox('Select series', series)
if selected_series:
    data = data[data['Series'] == selected_series]

recipients =  np.insert(recipients, 0, "all recipients")

selected_recipient = st.sidebar.multiselect('Select recipient', recipients)

st.sidebar.caption("""Beta ODA explorer development by Tomas Gonzalez using data from the OECD at https://stats.oecd.org/. 

This app is based on Streamlit and the source code is available at https://github.com/tomasgonz/oda. The source code is free to use, modify and distribute.""")

# ODA evolution
st.header("Distribution of aid by recipient")
st.write("""Distribution of net official development assistance (ODA) is defined as geographical aid allocations. 
Net ODA may be distributed by income group (least developed countries, other low-income countries, lower middle-income countries, upper middle-income countries, unallocated and more advanced developing countries and territories) or by geography (sub-Saharan Africa, South and Central Asia, other Asia and Oceania, Middle East and North Africa, Latin America and the Caribbean, Europe, and unspecified). The OECD Development Assistance Committee's "List of ODA Recipients" shows developing countries and territories eligible for ODA. The list is revised every three years. It is designed for statistical purposes, not as guidance for aid distribution or for other preferential treatment. 
In particular, geographical aid allocations are national policy decisions and responsibilities.""")

st.write("The chart below represets '" + selected_series +
     "' from '" + selected_donor + "' various groups of developing countries as reported to the DAC. The data is extracted from the DAC Geobook.")

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

if selected_recipient:
    for s in selected_recipient:
        fig_yearly.add_trace(get_trace(data[data['Recipient'] == s], s))

st.header("Aggregate aid to developing countries")

fig_yearly.update_layout(title='ODA to Developing Countries', xaxis_title='Year', 
    yaxis_title='ODA (USD)', height=600)

st.plotly_chart(fig_yearly, use_container_width=True)

# ODA evolution

# 2020
st.header(selected_donor + " - allocation of " + selected_series + "  by recipient")
st.write("The chart below shows reported flows in 2020 to individual countries. Note that for some countries a substantial volume of aid is reported as unspecified.")

data = data[~data['Recipient'].str.contains('Total')]
data = data[~data['Recipient'].str.contains('regional')]
data = data[~data['Recipient'].str.contains('WorldBank')]
data = data[~data['Recipient'].str.contains('World Bank')]
data = data[~data['Recipient'].str.contains('World Bank')]
data = data[~data['Recipient'].str.contains('Part')]
data = data[~data['Recipient'].str.contains('unspecified')]

data_2020 = data[data['Year'] == 2020].groupby(['Donor', 'Recipient'], as_index = False)['Value'].sum()
data_2020.sort_values(by=['Value'], inplace=True, ascending=False)

labels = data_2020['Recipient'].unique().tolist()

parents = [selected_donor] * len(labels)

fig = go.Figure(data=[go.Treemap(
    labels=labels,
    parents=parents,
    values=data_2020['Value']
)])

fig.update_layout(height=800)

st.plotly_chart(fig, font_size=10, use_container_width=True, height=2000)

st.subheader(selected_series + " - from " + selected_donor + " in 2020.")
st.table(data_2020[['Recipient', 'Value']])