import pyTigerGraph as tg

import streamlit as st
import pandas as pd

import configparser

import graphistry

#from functions import graph_overview

PAGE_CONFIG = {"page_title":"PlaNET","page_icon":":tiger:","layout":"wide"}
st.set_page_config(**PAGE_CONFIG)


def connect(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    
    conn = tg.TigerGraphConnection(host=config['tigergraph']['host'], 
                                   username=config['tigergraph']['username'],
                                   password=config['tigergraph']['password'], 
                                   useCert=True)

    graphistry.register(api=3, protocol="https", 
                        server=config['graphistry']['server'], 
                        username=config['graphistry']['username'], 
                        password=config['graphistry']['password'])
    return conn


def main():
    st.title("Tigyore Graph")

    pages = ["Graphistry", "Map View", "Bus Overview", "Train Overview", "Trip Drilldown", "Simulation"]
    conn = connect('configs.ini')
    selected_page = st.sidebar.selectbox('Pages',pages)
    

if __name__ == '__main__':
    main()