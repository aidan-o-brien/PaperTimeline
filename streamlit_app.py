import streamlit as st
import pandas as pd
import numpy as np
import plotly

from gather_data import *
from visualisation import *
from utils import update_bool


# -- Basic page display
apptitle = 'Research Timeline'
st.set_page_config(page_title=apptitle, page_icon="emojione:blue-book")

st.title('Research Timeline Visualisation')

st.markdown("""
    * Use the search box below to enter a DOI
    * Wait for a magical visualisation to appear
    * Use additional search functionality to filter for papers by terms in the
    title
""")


# -- Obtain DOI from user
doi = st.text_input("Please enter a DOI:", "")

if doi != "":
    # -- Obtain search filter from user
    search_query = st.text_input("Please enter a search term to filter papers:", "").lower()

    # -- Collect and process data
    df = create_df(doi)
    df = preprocess(df)

    if search_query == "":
        bool = np.ones(df.shape[0], dtype=bool)
    else:
        bool = update_bool(df, search_query)

    # -- Generate visualisation
    fig = create_viz(df[bool])
    st.plotly_chart(fig)
