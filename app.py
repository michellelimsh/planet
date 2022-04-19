import pyTigerGraph as tg

import streamlit as st
import pandas as pd

import configparser

import graphistry

PAGE_CONFIG = {"page_title":"PlaNET","page_icon":":tiger:","layout":"wide"}
st.set_page_config(**PAGE_CONFIG)


def connect(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    
    conn = tg.TigerGraphConnection(host=config['tigergraph']['host'], 
                                   graphname=config['tigergraph']['graph_name'],
                                   username=config['tigergraph']['username'],
                                   password=config['tigergraph']['password'])

    conn.apiToken = conn.getToken(config['tigergraph']['secret'])     
    

    graphistry.register(api=3, protocol="https", 
                        server=config['graphistry']['server'], 
                        username=config['graphistry']['username'], 
                        password=config['graphistry']['password'])
    return conn

conn = connect('configs.ini')

def run_query(query_name, params, output_name):
    results = conn.runInstalledQuery(query_name, params=params)
    df = pd.DataFrame(results[0][output_name])
    return df

def main():
    st.title("Tigyore Graph")
    pages = ["Centrality Analysis", "Service Similarity Analysis"]
    
    selected_page = st.sidebar.radio('Pages',pages)

    
    if selected_page == 'Centrality Analysis':
        option = st.selectbox('Select vertex to conduct centrality analysis on', ("TrainStation","BusStop","TrainService","BusService"))
        limit = st.number_input(label='max to display', value=10)
        if option == "TrainStation" or option == "BusStop":
            df = run_query("station_degree_centrality",
                           {'v_type':option, 'e_type':'waypoint', 'top_k':10},
                           "top_scores"
                            )
        elif option == "TrainService" or option == "BusService":
            df = run_query("service_degree_centrality",
                           {'v_type':option, 'e_type':'utilise', 'top_k':10},
                           "top_scores"
                            )
        else:
            print("Error")
        st.dataframe(df)

    elif selected_page == 'Service Similarity Analysis':
        option = st.selectbox('Select vertex to conduct similarity analysis on', ("TrainStation","BusStop","TrainService","BusService"))
        selected_vertex = st.text_input(label='input id of vertex')
        if option and selected_vertex:
            st.write('You have selected', option, selected_vertex)
            df = run_query("jaccard_similarity",
                            {'source':'1', 'source.type':'TrainStation', 'e_type':'serve', 'rev_e_type':'serve', 'top_k':10},
                            "Others"
                            )
            st.dataframe(df)


if __name__ == '__main__':
    main()