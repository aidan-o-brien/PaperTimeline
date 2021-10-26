import streamlit as st
import pandas as pd
import numpy as np
import plotly

from gather_data import *
from visualisation import *
from utils import *


# -- Basic page display
st.set_page_config(page_title='Research Timeline', page_icon="emojione:blue-book")

st.title('Research Timeline Visualisation')

st.markdown("""
    * Use the search box below to enter a DOI
    * Wait for a magical visualisation to appear
    * Use additional search functionality to filter for papers by terms in the
    title OR by authors - currently, cannot do both
""")


# -- Obtain DOI from user
doi = st.text_input("Please enter a DOI:", "")

if doi != "":

    # -- Collect and process data
    st.write('Collecting and processing data...')
    df = create_df(doi)
    df = preprocess(df)
    st.write('Data collected and processed.')

    # -- Obtain search filter from user
    search_query = st.text_input("Please enter a search term to filter papers:", "").lower() # use callback?

    if search_query == "":
        bool = np.ones(df.shape[0], dtype=bool)
    else:
        bool = create_search_filter(df, search_query)

    # -- Author dropdown filter
    ## List of author names to select from
    authors_list = df[bool]['author_names'].tolist()
    authors_set = list(set([x for l in authors_list for x in l]))
    authors_filter = st.multiselect('Select authors to filter by:',
                                    authors_set)  # list
    #print(authors_filter)

    ## Update boolean for filtering
    if len(authors_filter) != 0:
        bool = create_author_filter(df, authors_filter)


    # -- Generate visualisation
    fig = create_viz(df[bool])
    st.plotly_chart(fig)
