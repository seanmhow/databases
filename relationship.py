import streamlit as st
import pandas as pd
import selection
import numpy as np
import matplotlib.pyplot as plt
import queries as q
import altair as alt
import connect
import selection as s
import plotly.express as px

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
    durToStormA = alt.Chart(durToStorm_df).mark_bar().encode(x='STORMTYPE',y='DURATION', color='STORMTYPE').properties(title="Average Accident Duration during Storm Types", width=600).interactive()
    st.altair_chart(durToStormA)

    
    stormVsNorm = q.stormAccidentDurationVsAverage(minutes=hours * 60)
    stormVsNorm_df = callSql(stormVsNorm).copy()
    sDf = pd.DataFrame({
        'Categories' : ["*During Storm", "All"],
        'Average Accident Duration' : [stormVsNorm_df['SDURATION'][0], stormVsNorm_df['DURATION'][0]]
    })
    stormVsNormA = alt.Chart(sDf).mark_bar().encode(y='Categories',x='Average Accident Duration',color='Categories').properties(width = 600, title="Average Duration of Accidents During Storms").interactive()
    st.altair_chart(stormVsNormA)



    expAcc = q.stormAccidentsVsExpectedAccidents(minutes = hours * 60)
    expAcc_df = callSql(expAcc).copy()
    eDF = pd.DataFrame({
        'Categories' : ["*During Storm", "Expected"],
        'Number of Accidents' : [expAcc_df['ACCIDENTSDURINGSTORMS'][0],expAcc_df['EXPECTEDACCIDENTS'][0]]
    })
    expAccA = alt.Chart(eDF).mark_bar().encode(y='Categories',x='Number of Accidents', color='Categories').properties(width = 600, title="Number of Accidents During Storms vs Expected Accidents in Same Counties").interactive()
    st.altair_chart(expAccA)

    percentile = st.select_slider(label="Percentile Accident Count By County", options=list(np.arange(0, 100)), key=10)
    wc = q.worstCountiesToLive(accidentPercentile=percentile)
    wc_df = callSql(wc).copy()
    counties = s.getLocationData()
    fig = px.choropleth_mapbox(wc_df, geojson=counties, locations='FIPS', color='DAMAGE', title="Most Expensive Counties",
                        color_continuous_scale="Burg",
                        mapbox_style="carto-positron",
                        zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                        opacity=0.5,
                        hover_name="COUNTY",
                        hover_data=["STATE", "DAMAGE"],
                        labels={'COUNT':'Accident Count', 'COUNTY': 'County', "STATE" : "State"})
    st.write(fig)