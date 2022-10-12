import colorsys
from re import S
import sys
import os
from webbrowser import get
sys.path.append("../")
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.graph_objects as go
import random

data = pd.DataFrame()

data = pd.read_csv(os.path.join(os.path.dirname(__file__), "oda_by_sector.csv"))

st.set_page_config(layout="wide")

sectors = [110, 140, 230, 215, 310, 320, 330, 520, 600, 700]

years = data['Year'].unique()

data = data[data['SECTOR'].isin(sectors)]
data = data[data['Donor'] != 'Official Donors, Total']
data = data[data['Donor'] != 'DAC Countries, Total']

data = data[~data['Recipient'].str.contains('Total')]
data = data[~data['Recipient'].str.contains('regional')]
data = data[~data['Recipient'].str.contains('unspecified')]

all_sectors = data['Sector'].unique()
all_donors = data['Donor'].unique()
all_recipients = data['Recipient'].unique()

all_donors = np.insert(all_donors, 0, "all donors")

selected_donor = st.sidebar.selectbox('Donor', all_donors)

if selected_donor:
    if selected_donor != "all donors":
        data = data[data['Donor'].isin([selected_donor])]

# 2020 - Sectors
data_donors_sectors_2020 = data[data['Year'] == 2020]
data_donors_sectors_2020 = data.groupby(['Donor', 'Sector'], as_index = False).sum()

labels = data_donors_sectors_2020['Donor'].unique().tolist() + all_sectors.tolist()

index_source = []
for e in data_donors_sectors_2020['Donor'].values.tolist():
    index_source.append(labels.index(e))

index_destination = []
for e in data_donors_sectors_2020['Sector'].values.tolist():
    index_destination.append(labels.index(e))

st.header("How has the sectoral allocation of " + selected_donor + " evolved between 2011 and 2020?")

da = data.groupby(['Year','Sector'], as_index = False).sum()[['Sector', 'Year', 'Value']].sort_values(by=['Year', 'Value'], ascending = False)

col1, col2, col3, col4 = st.columns(4)

col1.metric(label='Largest sector in 2011', value=da[da['Year'] == 2011].iloc[0]['Sector'])
col2.metric(label='Largest sector in 2011', value=da[da['Year'] == 2011].iloc[0]['Value'])
col3.metric(label='Largest sector in 2020', value=da[da['Year'] == 2020].iloc[0]['Sector'])
col4.metric(label='Largest sector in 2020', value=da[da['Year'] == 2020].iloc[0]['Value'])

change_2011_2020 = da[da['Year'] == 2011]['Value'].sum().round(2) / da[da['Year'] == 2020]['Value'].sum().round(2)

col1.metric(label='Volume of aid in current US in 2011', value=da[da['Year'] == 2011]['Value'].sum().round(2))
col2.metric(label='Volume of aid in current US in 2020', value=da[da['Year'] == 2020]['Value'].sum().round(2))

col3.metric(label="Change", value = "{:.2f}%".format((1 - change_2011_2020) * 100))

st.vega_lite_chart(da, {
    'mark': {'type': 'line', 'tooltip': True, "interpolate": "monotone", "point": "True"},
    'encoding': {
        'x': {'field': 'Year', 'type' : 'ordinal' },
        'y': {'field': 'Value', 'type': 'quantitative'},
        'color': {'field': 'Sector', 'type': 'nominal'},
    },
}, use_container_width=True, height=800)

st.header("How is " + selected_donor + " allocating its aid by sector in 2020?")
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
        'value' : data_donors_sectors_2020['Value']
    }
)])

fig.update_layout(height=1000)

st.plotly_chart(fig, font_size=10, use_container_width=True, height=1000)

sorted_data_donors_sector_2020 = data_donors_sectors_2020[['Donor', 'Sector', "Value"]].sort_values(by=['Value'], ascending=False)

st.dataframe(sorted_data_donors_sector_2020, use_container_width=True)

st.header("Where is " + selected_donor + " sending its aid in 2020?")

# 2020
data_donors_recipient_2020 = data[data['Year'] == 2020]
data_donors_recipient_2020 = data.groupby(['Donor', 'Recipient'], as_index = False).sum()

labels =  data_donors_recipient_2020['Donor'].unique().tolist() + all_recipients.tolist()

index_source = []
for e in data_donors_recipient_2020['Donor'].values.tolist():
    index_source.append(labels.index(e))

index_destination = []
for e in data_donors_recipient_2020['Recipient'].values.tolist():
    index_destination.append(labels.index(e))

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
        'value' : data_donors_recipient_2020['Value']
    }
)])

fig.update_layout(height=1500)
st.plotly_chart(fig, font_size=10, use_container_width=True, height=2000)

st.header("Top recipients of " + selected_donor + " in 2020")

sorted_data_donors_recipient_2020 = data_donors_recipient_2020[['Donor', 'Recipient', 'Value']].sort_values(by=['Value'], ascending=False)

st.dataframe(sorted_data_donors_recipient_2020, use_container_width=True)

st.header("How have the trends of recipients of aid by " + selected_donor + " evolved from 2010 to 2020?")

st.vega_lite_chart(data, {
    'mark': {'type': 'line', 'tooltip': True, "interpolate": "monotone", "point": "True"},
    'encoding': {
        'x': {'field': 'Year', 'type' : 'ordinal' },
        'y': {'field': 'Value', 'type': 'quantitative', 'aggregate':'sum'},
        'color': {'field': 'Recipient', 'type': 'nominal'},
    },
}, use_container_width=True, height=800)