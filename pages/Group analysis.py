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
import urllib
import importlib
from data import get_oda_recipients
from paises import Countries
from paises import Groups
from paises.alias import get_alias

st.set_page_config(layout="wide")

data = get_oda_recipients()
series = data['Series'].unique()
selected_series = st.sidebar.selectbox('Select series', series)
if selected_series:
    data = data[data['Series'] == selected_series]

donors = data['Donor'].unique()
selected_donor = st.sidebar.selectbox('Select a donor', donors)
if selected_donor != "all donors":
        data = data[data['Donor'] == selected_donor]

def get_trace(data, name):
    return go.Scatter(x=data['Year'], y=data['Value'], name=name)


g = Groups()

fig_groups = go.Figure()

groups = [gr['acronym'] for gr in g]

data_groups = []

selected_groups = st.sidebar.multiselect('Select a group', groups)
if selected_groups:
    for gr in selected_groups:
        group_countries = g.get_group(gr)['names']
        group_countries_and_aliases = get_alias(group_countries)            
        data_groups.append({'acronym':gr, 'data':data[data['Recipient'].isin(group_countries_and_aliases)]})
       
for dg in data_groups: 
    fig_groups.add_trace(get_trace(dg['data'].groupby(['Year'], as_index = False)['Value'].sum(), dg['acronym']))

    
fig_groups.update_layout(title='ODA to Developing Countries', xaxis_title='Year', 
    yaxis_title='ODA (USD)', height=600)

st.plotly_chart(fig_groups, use_container_width=True)

for dg in data_groups:
    fig_group = go.Figure()
    data = dg['data']
    data.sort_values(by=['Value'], inplace=True, ascending=False)
    fig_group = go.Figure(data=go.Bar(x=data['Recipient'], y=data['Value']))

    fig_group.update_layout(title=dg['acronym'], xaxis_title='Year', yaxis_title='USD, constant prices')
    st.plotly_chart(fig_group, use_container_width=True)
