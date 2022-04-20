import pyTigerGraph as tg
import pandas as pd
from datetime import datetime, date
import configparser


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


def run_query(conn, query_name, params, output_name):
    results = conn.runInstalledQuery(query_name, params=params)
    # print(results[0]['top_scores'])
    df = pd.DataFrame(results[0][output_name])
    return df

    
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
    
    # Fetch trips
    trips = run_query(conn, "get_all_starting_locs", 
                      {"v_input":target,"v_input.type":service_vertex, "e_type":"utilise"}, 
                      's2')["attributes"].apply(pd.Series) 

    return target_service, target_stations[['v_id', 'name', 'latitude', 'longitude']], trips



def fetch_centriality_data(conn, limit):
    size= 0
    diff = limit - size
    k = diff
    while diff > 0:
      k += 1
      TrainStation =run_query(conn, "station_degree_centrality",
                     {'v_type':'TrainStation', 'e_type':'waypoint', 'top_k':k},
                     "top_scores"
                      )[['name', 'score']].drop_duplicates('name').reset_index(drop=True)
      size = TrainStation.shape[0]
      diff = limit - size

    BusStop =run_query(conn, "station_degree_centrality",
               {'v_type':'BusStop', 'e_type':'waypoint', 'top_k':limit},
               "top_scores"
                )[['Vertex_ID', 'score']]
    BusStop['Vertex_ID'] = BusStop['Vertex_ID'].astype(str)
    BusStop['name'] = BusStop['Vertex_ID'].str.replace('.0', '')

    TrainService =run_query(conn, "service_degree_centrality",
                   {'v_type':'TrainService', 'e_type':'utilise', 'top_k':limit},
                   "top_scores"
                    )[['Vertex_ID', 'score']].rename(columns={"Vertex_ID": "name"})

    BusService = run_query(conn, "service_degree_centrality",
                   {'v_type':'BusService', 'e_type':'utilise', 'top_k':limit},
                   "top_scores"
                    ).rename(columns={"Vertex_ID": "name"})#[['Vertex_ID', 'score']].rename(columns={"Vertex_ID": "name"})
    return TrainStation, BusStop[['name', 'score']], TrainService, BusService


def fetch_bus_services(conn):
    results = conn.runInstalledQuery("get_bus_services_with_trips")
    bus_services = [r["attributes"]["name"] for r in results[0]["result"] if r["attributes"]["name"]] 
    bus_services.sort()
    return bus_services


def fetch_neighbour_trips(conn, target, service_type):
    df = run_query(conn, "get_neighbour_vertices", 
            {"v_input":target,"v_input.type":service_type, "e_type":'utilise'}, 
            'result')["attributes"].apply(pd.Series)

    df['start'] = df['start_time'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
    df['end'] = df['end_time'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))

    df['start_time'] = df['start'].apply(lambda x: x.hour)
    df['end_time'] = df['end'].apply(lambda x: x.hour)

    df['travel_time'] = df['end'] - df['start']
    df['travel_time'] = df['travel_time'].apply(lambda x: x.seconds)
    return df


def fetch_all_trips(conn):
    trips = conn.getVertexDataframe('Trips', timeout=0)