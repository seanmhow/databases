import streamlit as st
import pandas as pd
import selection
import numpy as np
import matplotlib.pyplot as plt
import queries as q
import altair as alt
import connect

@st.cache
def callSql(query):
    cnct = connect.db()
    x= pd.read_sql(query, con=cnct)
    cnct.close()
    return x


# Minutes to HH:MM format for the select_slider
def mToHm(minutes):
    minutes = int(minutes)
    hours = str(int(minutes / 60))
    hours = hours if len(hours) > 1 else ("0" + hours)
    minutes = str(int(minutes % 60))
    minutes = minutes if len(minutes) > 1 else ("0" + minutes)
    return f"{hours}:{minutes}"


def app():
    st.title('Climate Impact on Accidents')

    # Select Slider for severity to storm query
    mins = st.select_slider(label="Time Duration", options=list(np.arange(1, 2880)), format_func=mToHm, key=0)

    durToStorm = q.accidentDurationToStorm(minutes=mins)
    durToStorm_df = callSql(durToStorm).copy()
    durToStormA = alt.Chart(durToStorm_df).mark_bar().encode(x='STORMTYPE',y='DURATION').properties(width=600).interactive()
    st.altair_chart(durToStormA)

    
    stormVsNorm = q.stormAccidentDurationVsAverage(minutes=mins)
    stormVsNorm_df = callSql(stormVsNorm).copy()
    sDf = pd.DataFrame({
        'Categories' : ["Storm", "All Accidents"],
        'Duration' : [stormVsNorm_df['SDURATION'][0], stormVsNorm_df['DURATION'][0]]
    })
    stormVsNormA = alt.Chart(sDf).mark_bar(size=30).encode(x='Categories',y='Duration').properties(width=600).interactive()
    st.altair_chart(stormVsNormA)



    expAcc = q.stormAccidentsVsExpectedAccidents(minutes = mins)
    expAcc_df = callSql(expAcc).copy()
    eDF = pd.DataFrame({
        'Categories' : ["During Storm", "Expected"],
        'Number of Accidents' : [expAcc_df['ACCIDENTSDURINGSTORMS'][0],expAcc_df['EXPECTEDACCIDENTS'][0]]
    })
    expAccA = alt.Chart(eDF).mark_bar(size=30).encode(x='Categories',y='Number of Accidents').properties(width=600).interactive()
    st.altair_chart(expAccA)

