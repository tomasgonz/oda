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

    The main motivation to create this page was to understand the dynamics of aid in relation to the leasts developed countries (LDCs).

    The LDCs are a group of countries that face structural challenges limiting their ability to develop (see https://www.un.org/development/desa/dpad/least-developed-country-category.html for more information on the LDCs).

    Although this site was not designed to explore regional or country group aid dynamics beyond the LDCs, some may find it useful to explore official aid dynamics to other groups.

    As with every piece of code, and certainly with virtually every piece of economic analysis, you will find errors and shortcomings. Please write to me with your suggestions to tomas@tomasgonzalez.net.

    Be well.

    T.

    """)

st.sidebar.success("Welcome to the ODA explorer. Use the options above to navigate through the various sections.")

st.sidebar.caption("""Beta ODA explorer development by Tomas Gonzalez using data from the OECD at https://stats.oecd.org/. 

This app is based on Streamlit and the source code is available at https://github.com/tomasgonz/oda. The source code is free to use, modify and distribute.""")
