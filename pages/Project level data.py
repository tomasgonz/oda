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
from data import get_crs
st.set_page_config(layout="wide")

data = get_crs()

donors = data['DonorName'].unique()

selected_donor = st.sidebar.selectbox('Select a donor', data['DonorName'].unique())
if selected_donor != "all donors":
        data = data[data['DonorName'] == selected_donor]

selected_recipients = st.sidebar.multiselect('Select recipients', data['RecipientName'].unique())
if selected_recipients:
        data = data[data['RecipientName'].isin(selected_recipients)]

flow_names = data['FlowName'].unique()
selected_flow = st.sidebar.selectbox('Select a flow', flow_names)
if selected_flow != "all flows":
        data = data[data['FlowName'] == selected_flow]

sector_names = data['SectorName'].unique()
purpose_names = data['PurposeName'].unique()

data
