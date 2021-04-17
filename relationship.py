import streamlit as st
import pandas as pd
import selection
import numpy as np
import matplotlib.pyplot as plt
import queries as q
import altair as alt

# Minutes to HH:MM format for the select_slider
def mToHm(minutes):
    minutes = int(minutes)
    hours = str(int(minutes / 60))
    hours = hours if len(hours) > 1 else ("0" + hours)
    minutes = str(int(minutes % 60))
    minutes = minutes if len(minutes) > 1 else ("0" + minutes)
    return f"{hours}:{minutes}"


def app(cnct):
    st.title('Climate Impact on Accidents')

    # Select Slider for severity to storm query
    mins = st.select_slider(label="Time Duration", options=list(np.arange(1, 2880)), format_func=mToHm, key=0)

    durToStorm = q.accidentDurationToStorm(minutes=mins)
    durToStorm_df = pd.read_sql(durToStorm, con=cnct)
    durToStormA = alt.Chart(durToStorm_df).mark_bar().encode(x='STORMTYPE',y='DURATION').properties(width=600)
   # st.write(durToStormA)

    
    mins2 = st.select_slider(label="Time Duration", options=list(np.arange(1, 2880)), format_func=mToHm, key=1)
    stormVsNorm = q.stormAccidentDurationVsAverage(minutes=mins2)
    stormVsNorm_df = pd.read_sql(stormVsNorm, con=cnct)
    sDf = pd.DataFrame({
        'a' : ["Storm", "All Accidents"],
        'b' : [stormVsNorm_df['SDURATION'][0], stormVsNorm_df['DURATION'][0]]
    })
    stormVsNormA = alt.Chart(sDf).mark_bar().encode(x='a',y='b').properties(width=600)
    st.write(stormVsNormA)
