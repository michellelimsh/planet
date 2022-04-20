import pyTigerGraph as tg
import pandas as pd

import configparser
import graphistry


def connect(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    
    conn = tg.TigerGraphConnection(host=config['tigergraph']['host'], 
                                   username=config['tigergraph']['username'],
                                   password=config['tigergraph']['password'])
    conn.graphname='TigyoreGraph'
    secret = conn.createSecret()
    authToken = conn.getToken(secret)
    authToken = authToken[0]
    conn = tg.TigerGraphConnection(host=config['tigergraph']['host'], 
                                   graphname='TigyoreGraph',
                                   username=config['tigergraph']['username'],
                                   password=config['tigergraph']['password'],
                                   apiToken=authToken)

#     graphistry.register(api=3, protocol="https", 
#                         server=config['graphistry']['server'], 
#                         username=config['graphistry']['username'], 
#                         password=config['graphistry']['password'])
    print('Connected')

    return conn
    
def fetch_map_data(conn, all_routes, station_vertex, service_vertex, target):
    # Filter services for chosen target
    target_service = all_routes[all_routes['v_id'] == target]

    # Fetch stations and edges
    stations = conn.getVertexDataframe(station_vertex, timeout=0)
    edges = conn.getEdgesDataframe(service_vertex, list(target_service["v_id"])[0])
    serves = edges[edges['to_type']==station_vertex]

    # Merge to get sequence
    station_ids = list(serves['to_id'])
    target_stations = pd.merge(stations[stations['v_id'].isin(station_ids)], serves, how='left', 
                               left_on='v_id', right_on='to_id').sort_values(by=['service_seq_no'])

    # Define path
    target_service['path'] = [target_stations[['longitude','latitude']].values.tolist()]

    return target_service, target_stations[['v_id', 'name', 'latitude', 'longitude']]



