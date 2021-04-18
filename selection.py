# This file is where we can add various select box queries if necessary. (States, Counties, Storm type, etc.)

import streamlit as st
import pandas as pd
import connect
from urllib.request import urlopen
import json

@st.cache
def callSql(query):
    cnct = connect.db()
    x = pd.read_sql(query, con=cnct)
    cnct.close()
    return x


def selectStates(key):
    states = """select distinct state from JPalavec.County WHERE state != 'AK' ORDER BY state asc"""
    df_states = callSql(states).copy()
    states_list = df_states['STATE'].to_list()
    states_list.insert(0,'All')
    state_box = st.selectbox('State', options=states_list, key=key)
    return state_box


def selectCounty(key,state='All'):
    county_list = ['All']
    if (state != 'All'):
        county = f"""select distinct County from Jpalavec.County WHERE State = '{state}' ORDER BY county asc"""
        df_county = callSql(county).copy()
        county_list = df_county['COUNTY'].to_list()
        county_list.remove('All')
        county_list.insert(0,'All')
    county_box = st.selectbox('County', options=county_list, key = key)
    return county_box


def selectStormType():
    storm_type = """select distinct StormType from Jpalavec.Storm"""
    df_storm_type = callSql(storm_type).copy()
    storm_type_box = st.selectbox("Storm Type", options=df_storm_type)
    return storm_type_box

@st.cache
def getLocationData():
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)
        return counties