import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np

from utils import functions as f
from utils import database_utils as db

from IPython.core.display import display, HTML

def render(conn):
    # Main
    st.header("Bus Network Analysis")
    
    all_routes = conn.getVertexDataframe('BusService', select='name', sort='name', timeout=0)
    all_routes = all_routes[all_routes['v_id'] != 'route_id']
    
    col1, padding, col2, col3 = st.columns([2,1, 1, 1])

    with col1:
        target = st.selectbox('Select a Bus Service', 
                          options=all_routes.v_id)
    try:
        routes, stations, trips = db.fetch_map_data(conn, all_routes, 'BusStop', 'BusService', target)
        with col2:
            st.metric("Trips", trips.shape[0])
        with col3:
            st.metric("Average Distance From Stop", "568 m")

        st.pydeck_chart(f.create_pydeck(routes, stations, trips))
        g = f.create_graph(stations, target)
        g.show('graphs/bus.html')
        HtmlFile = open('graphs/bus.html', 'r', encoding='utf-8')
        source_code = HtmlFile.read()

        components.html(source_code, height = 1200, width=1200)
    except:
        st.text('Found no trips, try a different service.')

