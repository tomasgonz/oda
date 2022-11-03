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
#series = data['Series'].unique()
#recipients = data['Recipient'].unique()

#data_selected_donor = data

selected_donor = st.sidebar.selectbox('Select a donor', donors)
if selected_donor != "all donors":
        data = data[data['DonorName'] == selected_donor]

data
