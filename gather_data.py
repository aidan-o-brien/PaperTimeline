"""A script to gather data from the Scopus database."""

import pandas as pd
from pybliometrics.scopus import ScopusSearch
import streamlit as st


def get_initial_paper(doi):
    '''Use the Scopus search API to find data on the user provided DOI
    (Digital Object Identifier). Returns a dataframe of the data provided
    by Scopus.'''

    # Search Scopus using ScopusSearch API
    query = f"DOI ({doi})"
    res = ScopusSearch(query)   # error here
    df = pd.DataFrame(res.results)

    # If doi is not valid
    if df.shape[0] == 0:
        return df

    # Split author data
    df.author_names = df.author_names.str.split(';')
    df.author_ids = df.author_ids.str.split(';')
    # Add paper key
    df['paper_key'] = 'origin paper'

    return df


def get_papers_by_authors(author_ids):
    '''Uses the Scopus database to find papers that are written by the authors
    of the origin (query) paper.

    ---WARNING---

    This Scopus functionality is in beta mode and it is expected that there
    are errors in the mapping of papers to authors.'''

    # Search for papers by authors of query paper
    st.write('Fetching papers by authors...')

    # Add a progress bar to help user know how long data collection takes
    my_bar = st.progress(0)
    num_authors = len(author_ids)

    for i, author_id in enumerate(author_ids):
        author_query = f"AU-ID ({author_id})"
        author_s = ScopusSearch(author_query)

        if i == 0:
            df = pd.DataFrame(author_s.results)
        else:
            df = pd.concat([df, pd.DataFrame(author_s.results)])

        perc_complete = (i + 1) / num_authors
        my_bar.progress(perc_complete)

    # Split author data
    df.author_names = df.author_names.str.split(';')
    df.author_ids = df.author_ids.str.split(';')
    # Add paper key
    df['paper_key'] = 'papers by authors'

    return df


def get_citing_papers(eid):
    '''Uses the Scopus database to find papers that cite the origin (query)
    paper. Users the EID, a Scopus-specific unique identifier of papers.

    ---WARNING---

    The citing papers that are retrieved are limited to papers that are within
    the Scopus database. This means that any citing papers that are not covered
    by Scopus will not appear in the results.'''

    st.write('Fetching citing papers...')
    cited_query = f"REF ({eid})"
    cited_s = ScopusSearch(cited_query)
    df = pd.DataFrame(cited_s.results)
    if df.shape[0] == 0:  # handle papers with no citations
        return df

    # Split author data
    df.author_names = df.author_names.str.split(';')
    df.author_ids = df.author_ids.str.split(';')
    # Add paper key
    df['paper_key'] = 'citing papers'

    return df


def create_df(doi):
    '''Consolidates origin paper, papers by authors and citing papers. Origin
    paper is provided by user input in the form of a DOI (Digital Object
    Identifier).

    --- WARNINGS---

    - This Scopus functionality is in beta mode and it is expected that there
    are errors in the mapping of papers to authors.
    - The citing papers that are retrieved are limited to papers that are within
    the Scopus database. This means that any citing papers that are not covered
    by Scopus will not appear in the results.'''

    # Find data on initial paper
    df = get_initial_paper(doi)
    if df.shape[0] == 0:
        return df

    # Find papers by authors of initial paper
    df1 = get_papers_by_authors(df.iloc[0]['author_ids'])

    # Find papers that cite initial paper
    df2 = get_citing_papers(df.iloc[0]['eid'])

    # Combine dfs and drop duplicates (if there are citing papers)
    if df2.shape[0] != 0:
        df = pd.concat([df, df1, df2])
        df.drop_duplicates(subset='eid', keep='first', inplace=True)
    else:
        df = pd.concat([df, df1])
        df.drop_duplicates(subset='eid', keep='first', inplace=True)

    return df
