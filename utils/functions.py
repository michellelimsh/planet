
import pydeck as pdk
import pandas as pd

from pyvis import network as net



def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def create_pydeck(routes, stops, locations):
    # Get lat lon of middle station as start view state
    mid = round(routes.shape[0]/2)
    view_lat = list(stops['latitude'])[mid]
    view_lon = list(stops['longitude'])[mid]

    view_state = pdk.ViewState(
        latitude=view_lat,
        longitude=view_lon,
        zoom=10
    )

    # add layers
    route_layer = pdk.Layer(
        type='PathLayer',
        data=routes,
        pickable=True,
        get_color=hex_to_rgb('#355956'),
        width_scale=20,
        width_min_pixels=2,
        get_path='path',
        get_width=5
    )

    stops_layer = pdk.Layer(
        type='ScatterplotLayer',
        data=stops,
        get_position=['longitude', 'latitude'],
        auto_highlight=True,
        get_radius=150,
        opacity=0.7,
        get_fill_color=hex_to_rgb('#5cb4a4'),
        pickable=True
    )

    locations_layer = pdk.Layer(
        type='ScatterplotLayer',
        data=locations,
        get_position=['longitude', 'latitude'],
        auto_highlight=True,
        get_radius=100,
        opacity=0.2,
        get_fill_color=hex_to_rgb('#BB86FC'),
        pickable=True
    )

    r = pdk.Deck(layers=[locations_layer, route_layer, stops_layer], initial_view_state=view_state)
    return r

def create_graph(data, target):
    g=net.Network(height='400px', width='100%',heading='')
    
    g.add_node(target, color = "green")

    to = data['name'].tolist()
    for station_name in to:
        g.add_node(station_name, color = "blue")
        g.add_edge(target,station_name, color = "blue")

    return g