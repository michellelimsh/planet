import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

from utils import functions as f
from utils import database_utils as db


def render(conn):
    # Main
    st.subheader("Train Overview")
    
    all_routes = conn.getVertexDataframe('TrainService', select='name', sort='name', timeout=0)
    all_routes = all_routes[all_routes['v_id'] != 'route_id']
    
    col1, padding, col2, col3 = st.columns([2,1, 1, 1])

    with col1:
        target = st.selectbox('Select a Train Service', 
                          options=all_routes.v_id)
    with col2:
        st.metric("Trips", "253")
    with col3:
        st.metric("Average Distance From Stop", "568 m")
    
    routes, stations = db.fetch_map_data(conn, all_routes, 'TrainStation', 'TrainService', target)
    locations = None
    st.pydeck_chart(f.create_pydeck(routes, stations, locations))