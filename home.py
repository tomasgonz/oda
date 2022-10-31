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

st.set_page_config(layout="wide")
st.title("ODA Dashboard")
st.subheader("Who gives what to whom.")
st.write(""" This page is developed to explore the datasets made publicly available by the OECD at https://stats.oecd.org. 
    The code is available at https://github.com/tomasgonz/oda and  you can download and modify it as you wish.
    """)
st.sidebar.success("Welcome to the ODA explorer. Created by Tomas Gonzalez. Contact me at tomas@tomasgonzalez.net. Use the options above to navigate through the various sections.")