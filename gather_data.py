import pandas as pd
from pybliometrics.scopus import ScopusSearch
from stqdm import stqdm
import streamlit as st


def get_initial_paper(doi):

    # Search Scopus using ScopusSearch API
    query = f"DOI ({doi})"
    s = ScopusSearch(query)
    df = pd.DataFrame(s.results)

    # Split author data
    df.author_names = df.author_names.str.split(';')
    df.author_ids = df.author_ids.str.split(';')
    # Add paper key
    df['paper_key'] = 'origin paper'

    return df


def get_papers_by_authors(author_ids):

    # Search for papers by authors of query paper
    st.write('Fetching papers by authors...')
    for i, author_id in enumerate(author_ids):
        author_query = f"AU-ID ({author_id})"
        author_s = ScopusSearch(author_query)

        if i == 0:
            df = pd.DataFrame(author_s.results)
        else:
            df = pd.concat([df, pd.DataFrame(author_s.results)])

    # Split author data
    df.author_names = df.author_names.str.split(';')
    df.author_ids = df.author_ids.str.split(';')
    # Add paper key
    df['paper_key'] = 'papers by authors'

    return df


def get_citing_papers(eid):
    cited_query = f"REF ({eid})"
    cited_s = ScopusSearch(cited_query)
    df = pd.DataFrame(cited_s.results)

    # Split author data
    df.author_names = df.author_names.str.split(';')
    df.author_ids = df.author_ids.str.split(';')
    # Add paper key
    df['paper_key'] = 'citing papers'

    return df


def create_df(doi):

    # Find data on initial paper
    df = get_initial_paper(doi)

    # Find papers by authors of initial paper
    df1 = get_papers_by_authors(df.iloc[0]['author_ids'])

    # Find papers that cite initial paper
    df2 = get_citing_papers(df.iloc[0]['eid'])

    # Combine dfs
    df = pd.concat([df, df1, df2])

    # Drop duplicates
    before = df.shape[0]
    df.drop_duplicates(subset='eid', keep='first', inplace=True)

    return df
