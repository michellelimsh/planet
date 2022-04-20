import pyTigerGraph as tg

import configparser
import graphistry


def connect(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    
    conn = tg.TigerGraphConnection(host=config['tigergraph']['host'], 
                                   username=config['tigergraph']['username'],
                                   password=config['tigergraph']['password'], 
                                   useCert=True)

#     graphistry.register(api=3, protocol="https", 
#                         server=config['graphistry']['server'], 
#                         username=config['graphistry']['username'], 
#                         password=config['graphistry']['password'])
    print('Connected')

    return conn


def fetch_bus_routes_data(conn):
	return conn.getVertexDataframe('TrainService', select='name', sort='name', timeout=0)
