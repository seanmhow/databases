import streamlit as st
import pandas as pd
import selection as s
import seaborn as sns
import datetime as dt
import numpy as np
import queries
import plotly.express as px
import altair as alt
import connect

@st.cache
def callSql(query):
    cnct = connect.db()
    x= pd.read_sql(query, con=cnct)
    cnct.close()
    return x


def app():

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
    # states = """select distinct state from JPalavec.County WHERE state != 'AK' ORDER BY state asc"""
    # df_states = callSql(states).copy()
    # states_list = df_states['STATE'].to_list()
    # states_list.insert(0,'All')
    # state = st.selectbox('State', options=states_list)

    st.text("""
            Lets explore some interesting trends about car accidents in the US. Here we can examine 
            population density of counties on the X axis and number of car accidents in our database
            on the Y axis. You can use the state selector to narrow the points down to counties of a 
            single state!""")
    state = s.selectStates(key= 1)
    popDensityQuery = queries.accidentsPopDensityGraph(state=state)
    df_popDensity = callSql(popDensityQuery).copy()
    a = alt.Chart(df_popDensity).mark_circle(size=60).encode(x='POPDENSITY',y='ACCIDENTCOUNT',tooltip=['COUNTY','STATE','POPDENSITY','ACCIDENTCOUNT'], opacity=alt.value(0.5), color=alt.value('pink')).interactive().properties(width=600, title="Population Density To Accidents Scatter Plot")
    st.altair_chart(a)

    counties = s.getLocationData()

    accidentsQuery = queries.accidentsFips()
    df_accidents = callSql(accidentsQuery).copy()
    df_accidents['FIPS'] = df_accidents['FIPS'].apply(lambda x : f'0{x}' if len(x) < 5  else x)
    df_accidents['Logarithmic Accidents']=np.log10(df_accidents['COUNT'])

    st.text("""
        This simple query allows us to view the distribution of accidents across the US. 
        We can zoom in, hover over a county to provide more details, and even save and 
        export images from the map.""")
    fig = px.choropleth_mapbox(df_accidents, geojson=counties, locations='FIPS', color='COUNT', title="Car Accident Count by County",
                           color_continuous_scale="Cividis",
                           mapbox_style="carto-positron",
                           range_color=(0,40000),
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                           hover_name="COUNTY",
                           hover_data=["STNAME", "COUNT"],
                           labels={'COUNT':'Accident Count', 'COUNTY': 'County', 'STNAME': 'State'})


    st.plotly_chart(fig)
    st.text("""
    Here we can see a slightly different map. The color represents accident count per capita.
    It is interesting to note the differences between this map and the previous, as it provides
    a new perspective on where the most people are affected by car accidents.""")
    fig2 = px.choropleth_mapbox(df_accidents, geojson=counties, locations='FIPS', color='COUNTPC',title= "Car Accident Count Per Capita by County",
                            color_continuous_scale="Hot",
                            mapbox_style="carto-positron",
                            zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                            opacity=0.5,
                            hover_name="COUNTY",
                            hover_data=["STNAME","COUNT"],
                            labels={'COUNTPC':'Accidents Per Capita', 'COUNTY': 'County', 'STNAME': 'State'})


    st.plotly_chart(fig2)
    st.text("""
    This is a fun little query which depicts the average temperature of accidents in each county.
    We can see a beautiful gradient as we move North across the US. It is interesting to see many
    of the Northmost counties still have relatively warm accidents. Further exploration could involve
    comparisons to average temperature in the region.""")
    fig3 = px.choropleth_mapbox(df_accidents, geojson=counties, locations='FIPS', color='AVTEMP', title="Average Temperature of Car Accidents by County",
                            color_continuous_scale="BlueRed",
                            mapbox_style="carto-positron",
                            range_color=(15,75),
                            zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                            opacity=0.5,
                            hover_name="COUNTY",
                            hover_data=["STNAME", "COUNT"],
                            labels={'COUNT':'Accident Count','AVTEMP': 'Average Temperature of Accidents', 'COUNTY': 'County', 'STATE': 'State'})

    st.plotly_chart(fig3)

    st.text("""
    Now that we have reviewed overview of some basic accident and weather data across the US,
    we can take a deeper dive into some more complicated queries. Use the left navigation menu to view
    our pages with queries regarding accidents, and accident/storm analysis.""")