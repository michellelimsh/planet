import pyTigerGraph as tg

import streamlit as st
import pandas as pd

import configparser

import graphistry

from pages import graphistry_page
from pages import bus_page
from pages import train_page
from pages import trip_page
from pages import simulation_page

#from functions import graph_overview

PAGE_CONFIG = {"page_title":"PlaNET","page_icon":":tiger:","layout":"wide"}
st.set_page_config(**PAGE_CONFIG)


# def connect(config_path):
#     config = configparser.ConfigParser()
#     config.read(config_path)
    
#     conn = tg.TigerGraphConnection(host=config['tigergraph']['host'], 
#                                    username=config['tigergraph']['username'],
#                                    password=config['tigergraph']['password'], 
#                                    useCert=True)

#     graphistry.register(api=3, protocol="https", 
#                         server=config['graphistry']['server'], 
#                         username=config['graphistry']['username'], 
#                         password=config['graphistry']['password'])
#     return conn


def main():
    st.sidebar.title("PlaNET")

    pages = ["About", "Graphistry", "Bus Overview", "Train Overview", "Trip Drilldown", "Simulation"]
    # conn = connect('configs.ini')
    conn = None
    page = st.sidebar.radio('Navigate', 
                        options=pages, # geospatial
                        index=0)
    # selected_page = st.sidebar.selectbox('Pages',pages)
    
    # # Pages
    if page.lower() == 'about':
        about = open('README.md', 'r')
        # print(about.read())
        st.markdown(about.read())
    elif page.lower() == 'graphistry':
        graphistry_page.render(conn)
    elif page.lower() == 'bus overview':
        bus_page.render(conn)
    elif page.lower() == 'train overview':
        train_page.render(conn)
    elif page.lower() == 'trip drilldown':
        trip_page.render(conn)
    elif page.lower() == 'simulation':
        simulation_page.render(conn)
    else:
        st.text('Page ' + page + ' is not implemented.')

if __name__ == '__main__':
    main()