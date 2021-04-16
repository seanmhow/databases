import streamlit as st
import pandas as pd
import selection
import numpy as np
import matplotlib.pyplot as plt
import queries as q


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
    mins = st.select_slider(label="Time Duration", options=list(np.arange(1, 2880)), format_func=mToHm)

    sbs_df = pd.read_sql(q.severityToStorm(mins), cnct)
    st.write(sbs_df)

    # Figure needs to be added here.
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
