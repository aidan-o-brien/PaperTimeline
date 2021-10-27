import streamlit as st
import pandas as pd
import numpy as np
import plotly

from gather_data import *
from visualisation import *
from utils import *
import base64


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
    df = create_df(doi)
    df = preprocess(df)
    st.write('Data collected and processed.')


    # -- Obtain search filter from user
    search_query = st.text_input("Please enter a search term to filter papers:", "").lower() # use callback?


    # -- Author dropdown filter
    ## List of author names to select from
    authors_list = df['author_names'].tolist()
    authors_set = list(set([x for l in authors_list for x in l]))
    authors_filter = st.multiselect('Select authors to filter by:',
                                    authors_set)  # list


    # -- Create a boolean array for filtering df
    if search_query != "" and len(authors_filter) != 0:
        filter_bool = create_author_filter(df, authors_filter)
        search_bool = create_search_filter(df, search_query)
        my_bool = np.logical_and(filter_bool, search_bool)
    elif search_query != "":
        my_bool = create_search_filter(df, search_query)
    elif len(authors_filter) != 0:
        my_bool = create_author_filter(df, authors_filter)
    else:
        my_bool = np.ones(df.shape[0], dtype=bool)


    # -- Generate visualisation
    origin_date = df[df['paper_key'] == 'origin paper']['month_year'][0]
    #fig = create_viz(df[my_bool], origin_date)
    #st.plotly_chart(fig)


    # -- Generate citation Visualisation
    fig_2 = create_cites_viz(df[my_bool], origin_date)
    st.plotly_chart(fig_2)


    # -- Option to download the fitlered dataframe
    st.markdown(get_table_download_link(df[my_bool]), unsafe_allow_html=True)


    # -- Option to view some summary statistics
    sum_stats = st.checkbox('Show summary statistics')
    placeholder = st.empty()
    if sum_stats:
        sum_stats_text = produce_sum_stats()
        placeholder.markdown(sum_stats_text)
