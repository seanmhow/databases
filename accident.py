import streamlit as st
import pandas as pd
import selection
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import queries as q


def app(cnct):
    st.title('Car Accidents')

    # Queries
    byMonth = q.hourMonthHeatmap()
    popDenHr = q.hourAverageDensityHeatmap("All")
    acla = q.accidentsPopDensityGraph()

    # create a text element and let the reader know that the data is loading
    data_load_state = st.text('loading accident data...')
    # load data into the dataframe

    # dataframes
    pdh_df = pd.read_sql(popDenHr, con=cnct)
    month_df = pd.read_sql(byMonth, con=cnct)
    acla_df = pd.read_sql(acla, con=cnct)

    # Population Density by Hour
    # pivot the data
    pdh_df = pd.pivot_table(pdh_df, index=['HOUR'], columns=['AVERAGEDENSITY'], values='COUNTS')

    # heatmaps
    fig2 = plt.figure()
    sns.heatmap(pdh_df)
    plt.title("Population Density by Hour")
    st.pyplot(fig2)

    st.write(pdh_df)

    # Month vs Hour
    month_df = pd.pivot_table(month_df, index=['HOUR'], columns=['MONTH'], values='COUNTS')

    fig3 = plt.figure()
    sns.heatmap(month_df)
    st.pyplot(fig3)

    st.write(month_df)

    # acla_df
    y = acla_df['ACCIDENTCOUNT'].to_numpy()
    x = acla_df['POPDENSITY'].to_numpy()
    fig1 = plt.figure()
    plt.scatter(x, y)
    st.pyplot(fig1)

    st.write(acla_df)

    # notify the reader that the data was successfully loaded
    data_load_state.text('Loading data...done!')
