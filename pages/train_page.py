import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk


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

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def create_pydeck(routes, stops, locations):
    routes['color'] = routes['color'].apply(hex_to_rgb)

    view_state = pdk.ViewState(
        latitude=37.782556,
        longitude=-122.3484867,
        zoom=10
    )

    route_layer = pdk.Layer(
        type='PathLayer',
        data=routes,
        pickable=True,
        get_color='color',
        width_scale=20,
        width_min_pixels=2,
        get_path='path',
        get_width=5
    )

    stops_layer = pdk.Layer(
        type='ScatterplotLayer',
        data=stops,
        get_position=['lon', 'lat'],
        auto_highlight=True,
        get_radius=150,
        opacity=0.7,
        get_fill_color='[255, 140, 0]',
        pickable=True
    )

    locations_layer = pdk.Layer(
        type='ScatterplotLayer',
        data=locations,
        get_position=['lon', 'lat'],
        auto_highlight=True,
        get_radius=100,
        get_fill_color='[180, 0, 200, 140]',
        pickable=True
    )

    r = pdk.Deck(layers=[route_layer, stops_layer, locations_layer], initial_view_state=view_state)
    return r


def render(conn):
    # Main
    st.subheader("Train Overview")
    routes = fetch_train_routes_data(conn)
    col1, padding, col2, col3 = st.columns([2,1, 1, 1])

    with col1:
        target = st.selectbox('Select A Train Service', 
                          options=routes.name)
    with col2:
        st.metric("Trips", "253")
    with col3:
        st.metric("Average Distance From Stop", "568 m")

    stations = fetch_train_stops_data(routes, target)
    locations = fetch_start_location_data(conn)

    st.pydeck_chart(create_pydeck(routes[routes['name'] == target], stations, locations))