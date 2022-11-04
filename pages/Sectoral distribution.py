from re import S
from webbrowser import get
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.graph_objects as go
from data import get_oda_sectors

st.set_page_config(layout="wide")

data = get_oda_sectors()

all_sectors = data['SECTOR'].unique()
all_sectors_descriptions = data['Sector'].unique()

odd_sectors = []
even_sectors = []

for i in all_sectors:
    if i % 2 == 1:
        odd_sectors.append(i)
    else:
        even_sectors.append(i)

sectors = odd_sectors

data = data[data['Year'] <= 2020]

years = data['Year'].unique()

data = data[data['SECTOR'].isin(sectors)]
data = data[data['Donor'] != 'Official Donors, Total']
data = data[data['Donor'] != 'DAC Countries, Total']

all_sectors = data['Sector'].unique()
all_donors = data['Donor'].unique()

all_donors = np.append(all_donors, "all donors")
all_sectors_descriptions = np.insert(all_sectors, 0, "all sectors")

selected_donor = st.sidebar.selectbox('Donor', all_donors)
if selected_donor:
    if selected_donor != "all donors":
        data = data[data['Donor'].isin([selected_donor])]

selected_sectors = st.sidebar.selectbox('Sector', all_sectors_descriptions)
if selected_sectors:
    if selected_sectors != "all sectors":
        data = data[data['Sector'] == selected_sectors]

# Data definitions and header

st.caption("""Beta ODA explorer development by Tomas Gonzalez using data from the OECD at https://stats.oecd.org/. 

This app is based on Streamlit and the source code is available at https://github.com/tomasgonz/oda. The source code is free to use, modify and distribute.""")

st.title("Aid (ODA) by sector and donor")

st.write(""" Official Development Assistance (ODA) is defined as those flows to developing countries and multilateral institutions provided by official agencies, including state and local governments, or by their executive agencies, each transaction of which meets the following tests: i) it is administered with the promotion of the economic development and welfare of developing countries as its main objective; and ii) it is concessional in character and conveys a grant element of at least 25 per cent. The data is in millions, current US. 

OECD (2022), "Data warehouse", OECD.Stat (database), https://doi.org/10.1787/data-00900-en (accessed on 12 October 2022). """
)

if data.empty:
    st.stop()

# 2020 - Sectors

data_2020 = data[data['Year'] == 2020].groupby(['Donor', 'Sector', 'Year'], as_index = False)['Value'].sum()

labels = data_2020['Donor'].unique().tolist() + all_sectors.tolist()

index_source = []
for e in data_2020['Donor'].values.tolist():
    index_source.append(labels.index(e))

index_destination = []
for e in data_2020['Sector'].values.tolist():
    index_destination.append(labels.index(e))

da = data.groupby(['Year','Sector'], as_index = False)['Value'].sum()[['Sector', 'Year', 'Value']].sort_values(by=['Year', 'Value'], ascending = False)

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
        'value' : data_2020['Value']
    }
)])

fig.update_layout(height=1000)

st.plotly_chart(fig, font_size=10, use_container_width=True, height=1000)