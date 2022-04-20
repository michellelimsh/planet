import streamlit as st
import pandas as pd
import numpy as np

from utils import functions as f
from utils import database_utils as db


def render(conn):
    # Main
    st.subheader("Bus Overview")

    all_routes = conn.getVertexDataframe('BusService', select='name', sort='name', timeout=0)
    
    col1, padding, col2, col3 = st.columns([2,1, 1, 1])

    with col1:
        target = st.selectbox('Select A Bus Service', 
                          options=all_routes.v_id)
    with col2:
        st.metric("Trips", "253")
    with col3:
        st.metric("Average Distance From Stop", "568 m")
    
    routes, stations = db.fetch_map_data(conn, all_routes, 'BusStop', 'BusService', target)
    locations = fetch_start_location_data(conn)

    # st.dataframe(stations)
    # st.dataframe(routes)

    st.pydeck_chart(f.create_pydeck(routes, stations, locations))


