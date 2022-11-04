from re import S
from webbrowser import get
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.graph_objects as go
from data import get_oda_recipients
from paises import Countries
from paises import Groups
from paises.alias import get_alias

st.set_page_config(layout="wide")

data = get_oda_recipients()

donors = data['Donor'].unique()
selected_donor = st.sidebar.selectbox('Select a donor', donors)
if selected_donor != "all donors":
        data = data[data['Donor'] == selected_donor]

series = data['Series'].unique()
selected_series = st.sidebar.selectbox('Select series', series)
if selected_series:
    data = data[data['Series'] == selected_series]

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
       

st.sidebar.caption("""Beta ODA explorer development by Tomas Gonzalez using data from the OECD at https://stats.oecd.org/. 

This app is based on Streamlit and the source code is available at https://github.com/tomasgonz/oda. The source code is free to use, modify and distribute.""")

# ODA evolution
st.header("An overview of the distribution of aid by group of countries")

st.write("""Distribution of net official development assistance (ODA) is defined as geographical aid allocations. 
Net ODA may be distributed by income group (least developed countries, other low-income countries, lower middle-income countries, upper middle-income countries, unallocated and more advanced developing countries and territories) or by geography (sub-Saharan Africa, South and Central Asia, other Asia and Oceania, Middle East and North Africa, Latin America and the Caribbean, Europe, and unspecified). The OECD Development Assistance Committee's "List of ODA Recipients" shows developing countries and territories eligible for ODA. The list is revised every three years. It is designed for statistical purposes, not as guidance for aid distribution or for other preferential treatment. 
In particular, geographical aid allocations are national policy decisions and responsibilities.""")


for dg in data_groups: 
    fig_groups.add_trace(get_trace(dg['data'].groupby(['Year'], as_index = False)['Value'].sum(), dg['acronym']))

if selected_groups:
    st.header(selected_series + ' to ' + ', '.join(selected_groups))
    fig_groups.update_layout(xaxis_title='Country', 
        yaxis_title='ODA (USD)', height=600)
    st.plotly_chart(fig_groups, use_container_width=True)
else:
    st.write(" <- Select a group to see the distribution of aid")

for dg in data_groups:
    fig_group = go.Figure()
    data = dg['data']
    data = data[data['Year'] == 2020]
    data.sort_values(by=['Value'], inplace=True, ascending=False)
    fig_group = go.Figure(data=go.Bar(x=data['Recipient'], y=data['Value']))

    fig_group.update_layout(title=dg['acronym'], xaxis_title='Country', yaxis_title='USD, constant prices')
    st.plotly_chart(fig_group, use_container_width=True)
