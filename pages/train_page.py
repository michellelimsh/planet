import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
import datetime


from utils import functions as f
from utils import database_utils as db

# from IPython.core.display import display, HTML



def render(conn):
    # Main
    st.header("Train Network Analysis")
    
    all_routes = conn.getVertexDataframe('TrainService', select='name', sort='name', timeout=0)
    all_routes = all_routes[all_routes['v_id'] != 'route_id']
    
    col1, padding, col2, col3, col4 = st.columns([2,1, 1, 1, 1])

    with col1:
        target = st.selectbox('Select a Train Service', 
                          options=all_routes.v_id)
    # try:
    # Fetch target data
    routes, stations, trips = db.fetch_map_data(conn, all_routes, 'TrainStation', 'TrainService', target)
    trip_times = db.fetch_neighbour_trips(conn, target, 'TrainService')

    # Display Metrics
    with col2:
        st.metric("Trips", trips.shape[0])
    with col3:
        st.metric("Stations", stations.shape[0])
    with col4:
        avg = round(sum(trip_times["travel_time"].tolist())/trip_times.shape[0])
        st.metric("Average Travel Time", str(datetime.timedelta(seconds=avg)))

    # Display Map
    st.pydeck_chart(f.create_pydeck(routes, stations, trips))

    # Display Histograms
    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(trip_times, x="start_time", title='Depature Time')
        st.plotly_chart(fig)
    with c2:
        fig = px.histogram(trip_times, x="travel_time", title='Travel Time')
        st.plotly_chart(fig)

        # g = f.create_graph(stations, target)
        # g.show('graphs/train.html')
        # HtmlFile = open('graphs/train.html', 'r', encoding='utf-8')
        # source_code = HtmlFile.read()

        # components.html(source_code, height = 1200, width=1200)
    # except:
    #     st.text('Found no trips, try a different service.')