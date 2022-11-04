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
data = data[~data['Donor'].str.contains('G7')]

data = data[data['Year'] == 2020]

data.sort_values(by=['Value'], inplace=True, ascending=False)

table1_1010 = data[data['TRANSACTYPE'] == 1010]
table1_1010_grouped = table1_1010.groupby(['Donor'])['Value'].sum().reset_index()
table1_1010_grouped.sort_values(by=['Value'], inplace=True, ascending=False)

st.header("Flows of aid from donors to recipients in 2020")

fig_yearly = go.Figure(data=go.Bar(x=table1_1010_grouped['Donor'], y=table1_1010_grouped['Value']))

fig_yearly.update_layout(title='Flows of aid in 2020', xaxis_title='Country', yaxis_title='USD')
st.plotly_chart(fig_yearly, use_container_width=True)

donors = data['Donor'].unique()
selected_donor = st.sidebar.selectbox('Select a donor', donors)
data = data[data['Donor'] == selected_donor]

fund_flows = data['Fund flows'].unique()
selected_fund_flow = st.sidebar.selectbox('Select a fund flow', fund_flows)
data = data[data['Fund flows'] == selected_fund_flow]

data = data[~data['Aid type'].str.contains('GNI')]

labels = data['Aid type'].unique().tolist()

all_sectors_ids = []

# This function searchs for parent sectors on the basis of the string
# passed following the format X.X.x.
def get_parent_sector(sector):
    for i in range(len(all_sectors_ids)):
        if sector in all_sectors_ids[i]:
            stem = all_sectors_ids[i].split('.')[len(all_sectors_ids[i].split('.'))-2] + "."
            return all_sectors_ids[i].replace(stem, "")

    return ""

# This function searchs for parent sectors on the basis of the string

for s in labels:
    all_sectors_ids.append(s.split(" ")[0])

parents = []
values = []

for index, row in data.iterrows():
    parents.append(get_parent_sector(row['Aid type']))
    values.append(row['Value'])

fig = go.Figure(data=[go.Treemap(
    labels=labels,
    parents=parents,
    values=data['Value']
)])

fig.update_layout(height=800)

st.plotly_chart(fig, use_container_width=True)

data

