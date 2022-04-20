import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

from utils import functions as f
from utils import database_utils as db


def fetch_train_routes_data(conn):
    DATA_URL = "https://raw.githubusercontent.com/uber-common/deck.gl-data/master/website/bart-lines.json"
    df = pd.read_json(DATA_URL)
    return df

def fetch_train_stops_data(routes, target):
    df = routes[routes['name'] == target]
    stops = pd.DataFrame(df['path'].tolist()[0], columns=['lon', 'lat'])
    return stops

def fetch_start_location_data(conn):
    df = pd.DataFrame(
         np.random.randn(1000, 2) / [50, 50] + [37.9368543, -122.3535832] ,
         columns=['lat', 'lon'])
    return df


def render(conn):
    # Main
    st.subheader("Train Overview")
    routes = fetch_train_routes_data(conn)
    col1, padding, col2, col3 = st.columns([2,1, 1, 1])

    with col1:
        target = st.selectbox('Select A Bus Service', 
                          options=routes.name)
    with col2:
        st.metric("Trips", "253")
    with col3:
        st.metric("Average Distance From Stop", "568 m")

    stations = fetch_train_stops_data(routes, target)
    locations = fetch_start_location_data(conn)

    st.pydeck_chart(f.create_pydeck(routes[routes['name'] == target], stations, locations))