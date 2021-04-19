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
    hours = st.select_slider(label="Storm Duration in Hours", options=list(np.arange(0, 49)),value=1, format_func=hToDh, key=0)

    durToStorm = q.accidentDurationToStorm(minutes=hours*60)
    durToStorm_df = callSql(durToStorm).copy()
    durToStormA = alt.Chart(durToStorm_df).mark_bar().encode(x='STORMTYPE',y='DURATION', color=alt.Color('STORMTYPE', legend = alt.Legend(labelFontSize=15))).properties(title="Average Accident Duration during Storm Types", width=600).interactive()
    st.altair_chart(durToStormA)

    
    stormVsNorm = q.stormAccidentDurationVsAverage(minutes=hours * 60)
    stormVsNorm_df = callSql(stormVsNorm).copy()
    sDf = pd.DataFrame({
        'Categories' : ["*During Storm", "All"],
        'Average Accident Duration' : [stormVsNorm_df['SDURATION'][0], stormVsNorm_df['DURATION'][0]]
    })
    stormVsNormA = alt.Chart(sDf).mark_bar().encode(y='Categories',x='Average Accident Duration',color=alt.Color('Categories', legend = alt.Legend(labelFontSize=15))).properties(width = 600, title="Average Duration of Accidents During Storms").interactive()
    st.altair_chart(stormVsNormA)

    expAcc = q.stormAccidentsVsExpectedAccidents(minutes = hours * 60)
    expAcc_df = callSql(expAcc).copy()
    eDF = pd.DataFrame({
        'Categories' : ["*During Storm", "Expected"],
        'Number of Accidents' : [expAcc_df['ACCIDENTSDURINGSTORMS'][0],expAcc_df['EXPECTEDACCIDENTS'][0]]
    })
    expAccA = alt.Chart(eDF).mark_bar().encode(y='Categories',x='Number of Accidents', color='Categories').properties(width = 600, title="Number of Accidents During Storms vs Expected Accidents in Same Counties").interactive()
    st.altair_chart(expAccA)



    counties = s.getLocationData()

    severity = st.radio("Select Accident Severity", ('1', '2', '3', '4', 'All'))
    if severity == 'All':
    
        stCountyAcdnt = q.stormCountyAccidentAll(minutes = hours * 60)
        stCountyAcdnt_df = callSql(stCountyAcdnt).copy()
        fig = px.choropleth_mapbox(stCountyAcdnt_df, geojson=counties, locations='FIPS', color='COUNT',
                                    color_continuous_scale="Cividis",
                                    mapbox_style="carto-positron",
                                    range_color=(0,stCountyAcdnt_df["COUNT"].max()),
                                    zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                                    opacity=0.5,
                                    hover_name="COUNTY",
                                    hover_data=["COUNT"],
                                    labels={'COUNT':'Number of Accidents', 'COUNTY': 'County', 'STATE': 'State'})
        fig.update_layout(title="<b>Severity of Accidents During Storms</b>")
        st.plotly_chart(fig)
    
    else:
        stCountyAcdnt = q.stormCountyAccident(minutes = hours * 60, severity = severity)
        stCountyAcdnt_df = callSql(stCountyAcdnt).copy()
        fig = px.choropleth_mapbox(stCountyAcdnt_df, geojson=counties, locations='FIPS', color='COUNT',
                                    color_continuous_scale="Cividis",
                                    mapbox_style="carto-positron",
                                    range_color=(0,stCountyAcdnt_df["COUNT"].max()),
                                    zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                                    opacity=0.5,
                                    hover_name="COUNTY",
                                    hover_data=["SEVERITY", "COUNT"],
                                    labels={'COUNT':'Number of Accidents', 'COUNTY': 'County', 'STATE': 'State'})
        fig.update_layout(title="<b>Severity of Accidents During Storms</b>")
        st.plotly_chart(fig)
    


    percentile = st.select_slider(label=f"Display counties in top X% of counties by Accident Count", options=list(np.arange(0, 100)), key=10)
    wc = q.worstCountiesToLive(accidentPercentile=percentile)
    wc_df = callSql(wc).copy()
    fig = px.choropleth_mapbox(wc_df, geojson=counties, locations='FIPS', color='DAMAGE', title="Most Expensive Counties",
                        color_continuous_scale="Burg",
                        mapbox_style="carto-positron",
                        zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                        opacity=0.5,
                        hover_name="COUNTY",
                        hover_data=["STATE", "DAMAGE"],
                        labels={'COUNT':'Accident Count', 'COUNTY': 'County', "STATE" : "State"})
    st.plotly_chart(fig)

