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
from data import get_oda_volume

st.set_page_config(layout="wide")

data = get_oda_volume()

st.header("ODA providers in 2020")
# ODA analysis
data = data[data['Amount type'] == 'Constant Prices']

data = data[~data['Donor'].str.contains('DAC')]

data = data[data['Year'] == 2020]

data.sort_values(by=['Value'], inplace=True, ascending=False)

table1_1010 = data[data['TRANSACTYPE'] == 1010]

fig_yearly = go.Figure(data=go.Bar(x=table1_1010['Donor'], y=table1_1010['Value']))

fig_yearly.update_layout(title='ODA (IA+IB) on', xaxis_title='Year', yaxis_title='USD, constant prices')
st.plotly_chart(fig_yearly, use_container_width=True)

donors = data['Donor'].unique()
selected_donor = st.sidebar.selectbox('Select a donor', donors)

transacts_bilateral = [1100, 1210, 1211, 1212, 1213, 1214, 1220, 1230, 1310, 1320, 1410, 1420, 1500, 1600, 1700, 1810, 1820, 1900 ]

transacts_multilateral = [2101, 2102, 2103, 2104, 2105,2106,2107,2108,2110]

transacts_debt = [301, 295]

transacts_inv = [340, 345, 751, 359]    

def get_fig_sector(transacts):
    filtered_data = data[data['TRANSACTYPE'].isin(transacts)]
    filtered_data = filtered_data[filtered_data['Year'] == 2020].groupby(['Aid type'])['Value'].sum().reset_index()
    
    fig = go.Figure(data=go.Pie(labels=filtered_data['Aid type'], values=filtered_data['Value']))

    return fig, filtered_data

fig = get_fig_sector(transacts_bilateral)[0]
fig.update_layout(title='ODA (IA) on', xaxis_title='Year', yaxis_title='USD, constant prices', showlegend=False, height=800)
fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig, use_container_width=True)

fig = get_fig_sector(transacts_multilateral)[0]
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.update_layout(title='ODA (IB) on', xaxis_title='Year', yaxis_title='USD, constant prices', showlegend=False, height=800)
st.plotly_chart(fig, use_container_width=True)

fig = get_fig_sector(transacts_inv)[0]
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.update_layout(title='ODA (Inv) on', xaxis_title='Year', yaxis_title='USD, constant prices', showlegend=False, height=800)

st.plotly_chart(fig, use_container_width=True)



