# This file is where we can add various select box queries if necessary. (States, Counties, Storm type, etc.)

import streamlit as st
import pandas as pd
import connect

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


def selectCounty():
    county = """select distinct County from Jpalavec.County"""
    df_county = pd.read_sql(county, cnct)
    county_box = st.selectbox('State', options=df_county)
    return county_box


def selectStormType():
    storm_type = """select distinct StormType from Jpalavec.Storm"""
    df_storm_type = pd.read_sql(storm_type, cnct)
    storm_type_box = st.selectbox("Storm Type", options=df_storm_type)
    return storm_type_box
