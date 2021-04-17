import streamlit as st
import pandas as pd
import selection
import seaborn as sns
import datetime as dt
import numpy as np
import queries
from urllib.request import urlopen
import json
import plotly.express as px
import altair as alt

def app(cnct):


    st.title('Overview')
    st.text('''
    Welcome to CrashDash, an analytics dashboard containing interesting
    findings related to accidents, storms, and population
    statistics across the United States.
    
    ''')



    # create a text element and let the reader know that the data is loading
    data_load_state_storm = st.text('loading storm data...')
    # load data into the dataframe

    # dataframes

    # notify the reader that the data was successfully loaded
    data_load_state_storm.text("")
    # select states
    states = """select distinct state from JPalavec.County WHERE state != 'AK' ORDER BY state asc"""
    df_states = pd.read_sql(states, cnct)
    states_list = df_states['STATE'].to_list()
    states_list.insert(0,'All')
    state = st.selectbox('State', options=states_list)
    popDensityQuery = queries.accidentsPopDensityGraph(state=state)
    df_popDensity = pd.read_sql(popDensityQuery, cnct)
    a = alt.Chart(df_popDensity).mark_circle(size=60).encode(x='POPDENSITY',y='ACCIDENTCOUNT',tooltip=['COUNTY','STATE','POPDENSITY','ACCIDENTCOUNT'], opacity=alt.value(0.2), color=alt.value('purple')).interactive().properties(width=600, title="Population Density To Accidents Scatter Plot")
    st.write(a)

    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

    accidentsQuery = queries.accidentsFips()
    df_accidents = pd.read_sql(accidentsQuery, cnct)
    df_accidents['FIPS'] = df_accidents['FIPS'].apply(lambda x : f'0{x}' if len(x) < 5  else x)
    df_accidents['Logarithmic Accidents']=np.log10(df_accidents['COUNT'])
    fig = px.choropleth_mapbox(df_accidents, geojson=counties, locations='FIPS', color='COUNT',
                           color_continuous_scale="Cividis",
                           mapbox_style="carto-positron",
                           range_color=(0,20000),
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                           hover_name="COUNTY",
                           hover_data=["STNAME", "COUNT"],
                           labels={'COUNT':'Accident Count', 'COUNTY': 'County', 'STNAME': 'State'})


    st.write(fig)

    fig2 = px.choropleth_mapbox(df_accidents, geojson=counties, locations='FIPS', color='COUNTPC',
                           color_continuous_scale="Hot",
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                           hover_name="COUNTY",
                           hover_data=["STNAME","COUNT"],
                           labels={'COUNTPC':'Accidents Per Capita', 'COUNTY': 'County', 'STNAME': 'State'})


    st.write(fig2)

    fig3 = px.choropleth_mapbox(df_accidents, geojson=counties, locations='FIPS', color='AVTEMP',
                            color_continuous_scale="BlueRed",
                            mapbox_style="carto-positron",
                            zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                            opacity=0.5,
                            hover_name="COUNTY",
                            hover_data=["STNAME", "COUNT"],
                            labels={'COUNT':'Accident Count','AVTEMP': 'Average Temperature of Accidents', 'COUNTY': 'County', 'STATE': 'State'})

    st.write(fig3)
    st.write(df_accidents)