"""A streamlit app that allows users to create a research timeline
visualisation for a paper within the Scopus database. The app also
provides some summary statistics, multiple filtering methods and the
ability to download data in csv format."""

import streamlit as st
import numpy as np

from gather_data import create_df
from visualisation import preprocess, create_cites_viz, create_wordcloud
from utils import (
    create_search_filter, create_author_filter, get_table_download_link, produce_sum_stats
)
from pybliometrics.scopus.exception import Scopus401Error


# -- Basic page display
st.set_page_config(page_title='Research Timeline', page_icon="emojione:blue-book")
st.title('Research Timeline Visualisation')


# 1) Obtain DOI from user input
doi = st.text_input("Please enter a DOI:", "")


# If user has input text, trying running
valid_doi = False
if doi:
    try:
        # 2) Collect and process data
        df = create_df(doi)
        df = preprocess(df)
        st.write('Data collected and processed.')
        valid_doi = True
    except KeyError:
        st.error('DOI not found. Please try again.')
    except Scopus401Error as err:
        from pathlib import Path
        config_location = str(Path.home()) + "\\"+ r'\.scopus\config.ini'
        st.error(f'Invalid API key. Make sure you are connected to the VPN of \
                   your institution. If you are, please consider updating your \
                   API key. You will be able to do this by creating a new API key \
                   on Scopus and updating it in the config file on your machine. \
                   This might be found under [Authenticaion] at the following \
                   location: {config_location}')
    #except:
        #st.error('There was an unexpected error.')


# If valid DOI provided, execute rest of program
if valid_doi:

    # 3) Provide options for filtering data - collapsable for aesthetics
    with st.expander('Search and Filter'):
        # Obtain search filter from user
        search_query = st.text_input("Search title and abstract:", "").lower()
        # Obtain author dropdown filter
        ## Create a list of author names to select from
        authors_list = df['author_names'].tolist()
        authors_set = list(set([x for l in authors_list for x in l]))
        authors_filter = st.multiselect('Select authors:',
                                        authors_set)  # list

    # Create a boolean array for filtering data
    if search_query != "" and authors_filter:
        filter_bool = create_author_filter(df, authors_filter)
        search_bool = create_search_filter(df, search_query)
        my_bool = np.logical_and(filter_bool, search_bool)
    elif search_query != "":
        my_bool = create_search_filter(df, search_query)
    elif authors_filter:
        my_bool = create_author_filter(df, authors_filter)
    else:
        my_bool = np.ones(df.shape[0], dtype=bool)


    # 4) Generate visualisation
    origin_date = df[df['paper_key'] == 'origin paper']['month_year'][0]
    fig = create_cites_viz(df[my_bool], origin_date)
    st.plotly_chart(fig)


    # 5) Option to download the fitlered dataframe
    st.markdown(get_table_download_link(df[my_bool]), unsafe_allow_html=True)


    # 6) Option to view some summary statistics
    with st.expander('Show Brief Summary'):
        origin_title = df[df['paper_key'] == 'origin paper']['title'][0]
        st.markdown(f"""## {origin_title} """)
        stats_markdown = produce_sum_stats(df)
        st.markdown(stats_markdown)
        st.markdown("""### Word Cloud of Abstracts """)
        wordcloud_fig = create_wordcloud(df)
        st.pyplot(wordcloud_fig)
