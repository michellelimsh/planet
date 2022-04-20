import streamlit as st
import pandas as pd
import numpy as np

from utils import functions as f
from utils import database_utils as db

import plotly.express as px

def render(conn):
    # Main
    st.header("Public Transport Network Analysis")
    st.subheader("")

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        st.metric("Trips", 25457)
    with c2:
        st.metric("Locations", 49857)
    with c3:
        st.metric("Train Services", 29)
    with c4:
        st.metric("Train Stations", 674)
    with c5:
        st.metric("Bus Services", 376)
    with c6:
        st.metric("Bus Stops", 12209 )

    st.subheader("")
    st.subheader("Centrality Analysis")

    limit = st.number_input(label='max to display', value=10)

    TrainStation, BusStop, TrainService, BusService = db.fetch_centriality_data(conn, limit)


    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(TrainStation, x='name', y='score', title="Train Stations")
        st.plotly_chart(fig)
        with st.expander('Top '+ str(limit) + ' Train Stations'):
            st.dataframe(TrainStation)

        fig = px.bar(BusStop, x='name', y='score', title='Bus Stops')
        st.plotly_chart(fig)
        with st.expander('Top '+ str(limit) + ' Bus Stops'):
            st.dataframe(BusStop)

    with c2:
        fig = px.bar(TrainService, x='name', y='score', title='Train Services')
        st.plotly_chart(fig)
        with st.expander('Top '+ str(limit) + ' Train Services'):
            st.dataframe(TrainService)

        fig = px.bar(BusService, x='name', y='score', title='Bus Services')
        st.plotly_chart(fig)
        with st.expander('Top '+ str(limit) + ' Bus Service'):
            st.dataframe(BusService)
