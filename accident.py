import streamlit as st
import pandas as pd
import selection
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import queries as q
import plotly.express as px


def app(cnct):
    st.title('Accident Analysis')
    #st.subtitle('What are the largest factors in causing')

    # Queries
    durStFips = q.accidentDurationState()
    sevStFips = q.accidentSeverityState()
    hourDay = q.hourWeekdayAccident()
    byMonth = q.hourMonthHeatmap()
    popDenHr = q.hourAverageDensityHeatmap()
    durHr = q.accidentDurationHourHeatmap()

    # create a text element and let the reader know that the data is loading
    data_load_state = st.text('loading accident data...')
    # load data into the dataframe

    # dataframes
    durStFips_df= pd.read_sql(durStFips, con=cnct)
    sevStFips_df = pd.read_sql(sevStFips, con=cnct)
    hourDay_df = pd.read_sql(hourDay,con=cnct)
    pdh_df = pd.read_sql(popDenHr, con=cnct)
    month_df = pd.read_sql(byMonth, con=cnct)
    durHr_df = pd.read_sql(durHr, con=cnct)

    #State accident duration map
    st.header("Average Accident Duration by State")
    st.text('''
    Accident duration refers to the time during which an accident impacts traffic flow
    The extremely high duration in some midwestern states is likely a result of certain
    accidents affecting infrastructure which can potentially impact a community for years.
    ''')
    fig = px.choropleth(durStFips_df,
                    locations='STATE',
                    color='AVDUR',
                    color_continuous_scale='spectral_r',
                    hover_name='STNAME',
                    locationmode='USA-states',
                    labels={'Current Unemployment Rate':'Unemployment Rate %'},
                    scope='usa')
    st.write(fig)


    st.header("Average Accident Severity by State")
    st.text('''
    Severity is also a metric which describes the impact of an accident on traffic, where 1
    is low impact with minimal delays, while 4 is severe impact.
    ''')
    fig = px.choropleth(sevStFips_df,
                    locations='STATE',
                    color='AVSEV',
                    color_continuous_scale='spectral_r',
                    hover_name='STNAME',
                    locationmode='USA-states',
                    labels={'Current Unemployment Rate':'Unemployment Rate %'},
                    scope='usa')
    st.write(fig)

    st.header('Accident Occurence Analysis')
    st.text('''
            Lets dive into some analysis of when and where these accidents are actually happening.
            A clear uptick of accident occurence appears in August as Summer comes to an end and
            everyone dives back into school.
    ''')
    # Month vs Hour
    month_df.rename(columns={'HOUR': 'Hour','MONTH' : 'Month'}, inplace=True)
    month_df = pd.pivot_table(month_df, index=['Hour'], columns=['Month'], values='COUNTS')

    fig1 = plt.figure()
    sns.heatmap(month_df, cmap="Blues")
    plt.title("Number of Accidents by Month and Hour")
    st.pyplot(fig1)

    st.text('''
           The proportion of accidents during weekdays to weekends is incredible!
           It also appears that accidents are more frequent on the front half of 
           the week than the last half. Rush hour AM and PM are clearly visible.
           Notice the lack of uptick on the weekends during these times.
    ''')
    #Hour vs Day of week
    hourDay_df.rename(columns={'HOUR': 'Hour','INDEXDAY' : 'Day of Week'}, inplace=True)
    hourDay_df = pd.pivot_table(hourDay_df, index=['Hour'], columns=['Day of Week'], values='COUNTS')
    fig2 = plt.figure()
    sns.heatmap(hourDay_df, xticklabels=['Sun','Mon','Tues','Wed','Thurs','Fri','Sat'], cmap="RdPu")
    plt.title("Number of Accidents by Day of Week and Hour")
    st.pyplot(fig2)
    
    st.text('''
           This graph is a bit tricky, each section on the x-axis contains 10% \of counties
           grouped by population density. The average popualtion density of that group is the
           x-tick on the bottom. It appears the top 10% most dense counties account for nearly
           every accident!
    ''')
    # Population Density by Hour
    # pivot the data
    pdh_df.rename(columns={'HOUR': 'Hour','AVERAGEDENSITY' : 'Average Density of 10th Percentiles'}, inplace=True)
    pdh_df = pd.pivot_table(pdh_df, index=['Hour'], columns=['Average Density of 10th Percentiles'], values='COUNTS')

    # heatmaps
    fig3 = plt.figure()
    sns.heatmap(pdh_df,xticklabels=pdh_df.columns.values.astype(int), cmap="YlGn")
    plt.title("Number of Accidents by Population Density and Hour")
    st.pyplot(fig3)

    st.text('''
          Finally this heatmap shows us how frequent accident durations occur throughout the day.
          The most frequent accidents take around 29 minutes to resume the normal flow of traffic, and occur
          at morning rush hour.
    ''')
    fig4 = plt.figure()
    durHr_df.rename(columns={'HOUR': 'Hour', 'AVERAGEDURATION': 'Average Duration of 10th Percentiles'}, inplace=True)
    durHr_df = pd.pivot_table(durHr_df, index=['Hour'], columns=['Average Duration of 10th Percentiles'], values='COUNTS')
    print(durHr_df.columns)
    sns.heatmap(durHr_df,xticklabels=durHr_df.columns.values.round(1), cmap = 'YlGnBu')
    plt.title("Number of Accidents by Hour and Duration")
    st.pyplot(fig4)
    # notify the reader that the data was successfully loaded
    data_load_state.text('Loading data...done!')


