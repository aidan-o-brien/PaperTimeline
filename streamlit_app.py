import streamlit as st
import pandas as pd
import plotly

from gather_data import *
from visualisation import *


# -- Set page config
apptitle = 'Research Timeline'
st.set_page_config(page_title=apptitle, page_icon="emojione:blue-book")

# -- Title the app
st.title('Research Timeline Visualisation')

st.markdown("""
    * Use the search box below to enter a DOI
    * Wait for a magical visualisation to appear
""")


# -- Obtain data
doi = st.text_input("Please enter a DOI:", "")

if doi != "":
    df = create_df(doi)


    # -- Generate visusalisation
    df = preprocess(df)
    fig = create_viz(df)
    st.plotly_chart(fig)
