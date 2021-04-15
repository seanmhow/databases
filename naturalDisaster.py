import streamlit as st
import pandas as pd
import selection
import seaborn as sns
import datetime as dt
import numpy as np


def app(cnct):
    st.title('Natural Disaster')
    stormQuery = """SELECT *
                    FROM JPALAVEC.STORM
                    ORDER BY 1 ASC
                        FETCH FIRST 100 ROWS ONLY"""

    # create a text element and let the reader know that the data is loading
    data_load_state_storm = st.text('loading storm data...')
    # load data into the dataframe

    # dataframes
    df_storm = pd.read_sql(stormQuery, con=cnct)

    # notify the reader that the data was successfully loaded
    data_load_state_storm.text('Loading data...done!')
    st.subheader('Storm Data')
    st.write(df_storm)

    # select states
    states = """select distinct State from JPalavec.County"""
    df_states = pd.read_sql(states, cnct)
    state = st.selectbox('State', options=df_states)
