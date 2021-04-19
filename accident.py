import streamlit as st
import pandas as pd
import selection as s
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import queries as q
import plotly.express as px
import connect

@st.cache
def callSql(query):
       cnct = connect.db()
       x = pd.read_sql(query, con=cnct)
       cnct.close()
       return x


def app():
       st.title('Accident Analysis')
       #st.subtitle('What are the largest factors in causing')

       #State selector

       # Queries
       durStFips = q.accidentDurationState()
       sevStFips = q.accidentSeverityState()
       hourDay = q.hourWeekdayAccident()


       # create a text element and let the reader know that the data is loading
       data_load_state = st.text('loading accident data...')
       # load data into the dataframe

       # dataframes
       durStFips_df= callSql(durStFips).copy()
       sevStFips_df = callSql(sevStFips).copy()

       #State accident duration map
       st.header("Average Accident Duration by State (minutes)")
       st.text('''
       Accident duration refers to the time during which an accident impacts traffic flow
       The extremely high duration in some midwestern states is likely a result of certain
       accidents affecting infrastructure which can potentially impact a community for years.
       ''')
       def strfdelta(tdelta):
              fmt = "{days} days {hours}:{minutes}:{seconds}"
              d = {"days": tdelta.days}
              d["hours"], rem = divmod(tdelta.seconds, 3600)
              d["minutes"], d["seconds"] = divmod(rem, 60)
              return fmt.format(**d)
       durStFips_df['MAXDUR'] = pd.to_timedelta(durStFips_df['MAXDUR'], unit='m')
       durStFips_df['MAXDUR'] =  durStFips_df['MAXDUR'].apply(strfdelta)


       fig = px.choropleth(durStFips_df,
                     title="Average Accident Impact on Traffic (minutes)",
                     locations='STATE',
                     color='AVDUR',
                     color_continuous_scale='spectral_r',
                     hover_name='STNAME',
                     hover_data=['MAXDUR','AVDUR'],
                     locationmode='USA-states',
                     labels={'AVDUR':'Average Duration', "MAXDUR":"Max Duration"},
                     scope='usa')
       st.plotly_chart(fig)


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
       st.plotly_chart(fig)

       state = s.selectStates(key= 2)
       county = s.selectCounty(key=3,state=state)
       byMonth = q.hourMonthHeatmap(state,county=county)
       
       hourDay_df = callSql(hourDay).copy()
       
       month_df = callSql(byMonth).copy()




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
              This heatmap shows us how frequent accident durations occur throughout the day.
              The most frequent accidents take around 29 minutes to resume the normal flow of traffic, and occur
              at morning rush hour.
       ''')


       percentile = st.select_slider(label="Number of Percentile Groups", options=list(np.arange(0, 21)),value=10, key=20)
       popDenHr = q.hourAverageDensityHeatmap(state, percentile=percentile)
       durHr = q.accidentDurationHourHeatmap(state,county=county,percentile = percentile)
       durHr_df = callSql(durHr).copy()
       pdh_df = callSql(popDenHr).copy()
       #print(len(durHr_df['AVERAGEDURATION'].unique()))
       #Hour and Duration
       fig4 = plt.figure()
       durHrTitles = np.sort(durHr_df.loc[:,['DURPERCENTILE','AVERAGEDURATION']].drop_duplicates().values[:,1].round(1))
       xticklabels = []
       for i in durHrTitles:
              if i%1 == 0:
                     xticklabels.append(int(i))
              else:
                     xticklabels.append(np.format_float_positional(i))
       print(durHrTitles)
       durHr_df.rename(columns={'HOUR': 'Hour', 'DURPERCENTILE': f'Average Duration of {int(100/percentile)}th Percentiles'}, inplace=True)
       durHr_df = pd.pivot_table(durHr_df, index=['Hour'], columns=[f'Average Duration of {int(100/percentile)}th Percentiles'], values='COUNTS')
       sns.heatmap(durHr_df,xticklabels=xticklabels, cmap = 'YlGnBu')
       plt.title("Number of Accidents by Hour and Duration")
       st.pyplot(fig4)


       # Population Density by Hour

       st.text('''
              This graph is a bit tricky, each section on the x-axis contains X% \of counties
              (defined by the slider) grouped by population density. The average popualtion
              density of that group is the x-tick on the bottom. It appears the top X% most
              dense counties account for nearly every accident!
       ''')

       # pivot the data
       pdh_df.rename(columns={'HOUR': 'Hour','AVERAGEDENSITY' : f'Average Density of {int(100/percentile)}th Percentile Counties'}, inplace=True)
       pdh_df = pd.pivot_table(pdh_df, index=['Hour'], columns=[f'Average Density of {int(100/percentile)}th Percentile Counties'], values='COUNTS')

       # heatmaps
       fig3 = plt.figure()
       sns.heatmap(pdh_df,xticklabels=pdh_df.columns.values.astype(int), cmap="YlGn")
       plt.title("Number of Accidents by Population Density and Hour")
       st.pyplot(fig3)
       # notify the reader that the data was successfully loaded
       data_load_state.text('')

       


