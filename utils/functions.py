
import pydeck as pdk
import pandas as pd


def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def create_pydeck(routes, stops, locations):
    # routes['color'] = routes['color'].apply(hex_to_rgb)
    mid = round(routes.shape[0]/2)
    view_lat = list(stops['latitude'])[mid]
    view_lon = list(stops['longitude'])[mid]

    view_state = pdk.ViewState(
        latitude=view_lat,
        longitude=view_lon,
        zoom=10
    )

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
        get_position=['lon', 'lat'],
        auto_highlight=True,
        get_radius=100,
        get_fill_color='[180, 0, 200, 140]',
        pickable=True
    )

    r = pdk.Deck(layers=[route_layer, stops_layer, locations_layer], initial_view_state=view_state)
    return r
