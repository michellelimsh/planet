import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px

from utils import functions as f
from utils import database_utils as db

from IPython.core.display import display, HTML

def render(conn):
    # Main
    st.header("Bus Network Analysis")
    
    # Fetch data
    all_routes = conn.getVertexDataframe('BusService', select='name', sort='name', timeout=0)
    bus_services = db.fetch_bus_services(conn)

    col1, padding, col2, col3 = st.columns([2,1, 1, 1])

    with col1:
        target = st.selectbox('Select a Bus Service', 
                          options=bus_services)

    # Fetch data from target
    trip_times = db.fetch_neighbour_trips(conn, target, 'BusService')
    routes, stations, trips = db.fetch_map_data(conn, all_routes, 'BusStop', 'BusService', target)

    with col2:
        st.metric("Trips", trips.shape[0])
    with col3:
        st.metric("Average Distance From Stop", "568 m")

    # Trip start time histogram
    c1, c2 = st.columns(2)
    # trip_times['travel_time'] = trip_times['end'] - trip_times['start']
    st.dataframe(trip_times)
    with c1:
        fig = px.histogram(trip_times, x="start_time", title='Depature time')
        st.plotly_chart(fig)
    # with c2:
    #     fig = px.histogram(trip_times, x="travel_time", title='Travel time')
    #     st.plotly_chart(fig)

    # Map
    # st.pydeck_chart(f.create_pydeck(routes, stations, trips))

    # Network graph
    # g = f.create_graph(stations, target)
    # g.show('graphs/bus.html')
    # HtmlFile = open('graphs/bus.html', 'r', encoding='utf-8')
    # source_code = HtmlFile.read()
    # components.html(source_code, height = 1200, width=1200)
    # except:
    #     st.text('Found no trips, try a different service.')

