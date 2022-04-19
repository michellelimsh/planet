import pyTigerGraph as tg

import streamlit as st
import pandas as pd

import graphistry

@st.cache
def graph_overview():
    return graph