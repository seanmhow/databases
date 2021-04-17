# Author: Sean Howard
# Date: 3/20/2021
# Citations: https://discuss.streamlit.io/t/how-to-link-a-button-to-a-webpage/1661/3 ,
#            https://medium.com/@u.praneel.nchar/building-multi-page-web-app-using-streamlit-7a40d55fa5b4 ,
#            https://discuss.streamlit.io/t/datetime-slider/163/7 ,


import streamlit as st
import multiapp
import naturalDisaster
import accident
import relationship
import connect
import datetime

st.set_page_config(page_title='Databases')

# connect to the DB
cnct = connect.db()

PAGES = {
    "Overview": naturalDisaster,
    "Accident Analysis": accident,
    "Storms and Accidents": relationship
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app(cnct)
