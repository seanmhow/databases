# This file is where we can add various select box queries if necessary. (States, Counties, Storm type, etc.)

import streamlit as st
import pandas as pd


def selectStates(cnct):
    states = """select distinct State from JPalavec.County"""
    df_states = pd.read_sql(states, cnct)
    state_box = st.selectbox('State', options=df_states)
    return state_box


def selectCounty(cnct):
    county = """select distinct County from Jpalavec.County"""
    df_county = pd.read_sql(county, cnct)
    county_box = st.selectbox('State', options=df_county)
    return county_box


def selectStormType(cnct):
    storm_type = """select distinct StormType from Jpalavec.Storm"""
    df_storm_type = pd.read_sql(storm_type, cnct)
    storm_type_box = st.selectbox("Storm Type", options=df_storm_type)
    return storm_type_box
