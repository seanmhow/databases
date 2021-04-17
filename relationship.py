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
def hToDh(hours):
    hours = int(hours)
    days = str(int(hours / 24))
    days = days if len(days) > 1 else ("0" + days)
    hours = str(int(hours % 24))
    hours = hours if len(hours) > 1 else ("0" + hours)
    return f"{days}:{hours} "


def app():
    st.title('Climate Impact on Accidents')

    # Select Slider for severity to storm query
    hours = st.select_slider(label="Storm Duration in Hours", options=list(np.arange(1, 49)), format_func=hToDh, key=0)

    durToStorm = q.accidentDurationToStorm(minutes=hours*60)
    durToStorm_df = callSql(durToStorm).copy()
    durToStormA = alt.Chart(durToStorm_df).mark_bar().encode(x='STORMTYPE',y='DURATION').properties(width=600).interactive()
    st.altair_chart(durToStormA)

    
    stormVsNorm = q.stormAccidentDurationVsAverage(minutes=hours * 60)
    stormVsNorm_df = callSql(stormVsNorm).copy()
    sDf = pd.DataFrame({
        'Categories' : ["Storm", "All Accidents"],
        'Duration' : [stormVsNorm_df['SDURATION'][0], stormVsNorm_df['DURATION'][0]]
    })
    stormVsNormA = alt.Chart(sDf).mark_bar(size=30).encode(x='Categories',y='Duration').properties(width=600).interactive()
    st.altair_chart(stormVsNormA)



    expAcc = q.stormAccidentsVsExpectedAccidents(minutes = hours * 60)
    expAcc_df = callSql(expAcc).copy()
    eDF = pd.DataFrame({
        'Categories' : ["During Storm", "Expected"],
        'Number of Accidents' : [expAcc_df['ACCIDENTSDURINGSTORMS'][0],expAcc_df['EXPECTEDACCIDENTS'][0]]
    })
    expAccA = alt.Chart(eDF).mark_bar(size=30).encode(x='Categories',y='Number of Accidents').properties(width=600).interactive()
    st.altair_chart(expAccA)

