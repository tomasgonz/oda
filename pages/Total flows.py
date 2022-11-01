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

fig_yearly.update_layout(title='Flows of aid in 2020', xaxis_title='Year', yaxis_title='USD')
st.plotly_chart(fig_yearly, use_container_width=True)

donors = data['Donor'].unique()
selected_donor = st.sidebar.selectbox('Select a donor', donors)
data = data[data['Donor'] == selected_donor]

fund_flows = data['Fund flows'].unique()
selected_fund_flow = st.sidebar.selectbox('Select a fund flow', fund_flows)
data = data[data['Fund flows'] == selected_fund_flow]

data = data[~data['Aid type'].str.contains('GNI')]


labels = data['Aid type'].unique().tolist()

labels

parents = [selected_donor, "V. Net Private Grants (V.1 minus V.2)"]

data

fig = go.Figure(data=[go.Treemap(
    labels=labels,
    parents=parents,
    values=data['Value']
)])

fig.update_layout(height=800)

st.plotly_chart(fig, use_container_width=True)

data

