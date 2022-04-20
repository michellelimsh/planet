import streamlit as st
import pandas as pd

from utils import database_utils as db

from pages import public_transport_page
from pages import bus_page
from pages import train_page


PAGE_CONFIG = {"page_title":"PlaNET","page_icon":":tiger:","layout":"wide"}
st.set_page_config(**PAGE_CONFIG)


def main():

    pages = ["About", "Public Transport", "Bus", "Train"]
    conn = db.connect('configs.ini')

    st.sidebar.title("PlaNET")
    page = st.sidebar.radio('Navigate', 
                        options=pages,
                        index=0)
    
    # Pages
    if page.lower() == 'about':
        about = open('README.md', 'r')
        st.markdown(about.read())
    elif page.lower() == 'public transport':
        public_transport_page.render(conn)
    elif page.lower() == 'bus':
        bus_page.render(conn)
    elif page.lower() == 'train':
        train_page.render(conn)
    else:
        st.text('Page ' + page + ' is not implemented.')

if __name__ == '__main__':
    main()