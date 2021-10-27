import pandas as pd
import numpy as np
import base64


def create_search_filter(df, query):

    # Search through title and abstract
    title_bool = df['title'].str.contains(query, case=False, regex=False)
    abstract_bool = df['description'].str.contains(query, case=False, regex=False)

    # Convert to np arrays for boolean logic
    title_bool = title_bool.to_numpy(dtype=bool)
    abstract_bool = abstract_bool.to_numpy(dtype=bool)

    return np.logical_or(title_bool, abstract_bool)


def create_author_filter(df, authors_filter):
    temp_df = df.explode('author_names')

    # for each author, filter df for just their papers
    indices = []
    for author in authors_filter:
        author_indices = temp_df[temp_df['author_names'] == author].index.to_numpy()
        for idx in author_indices:
            indices.append(idx)
    # We only care about unique papers, no duplicates
    indices = set(indices)
    index_array = np.zeros(df.shape[0], dtype=bool)
    for idx in indices:
        index_array[idx] = 1

    return index_array


def get_table_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="research_timeline.csv">Download data</a>'
    return href


def produce_sum_stats(df):
    origin_paper = df[df['paper_key'] == 'origin paper']
    title = origin_paper['title'][0]
    # authors
    authors = origin_paper['author_names'][0]
    authors_str = ''
    for i, name in enumerate(authors):
        if i == len(authors) - 1:
            authors_str += name
        else:
            authors_str += f'{name}; '
    num_papers_by_authors = df[df['paper_key'] == 'papers by authors'].shape[0]
    num_papers_citing = df[df['paper_key'] == 'citing papers'].shape[0]
    cites = df['citedby_count'].to_numpy(dtype=np.float)
    mean_cites = cites.mean()
    max_cites = cites.max()
    temp_df = df.explode('author_names')
    num_authors = len(temp_df.author_names.unique())

    markdown = f"""
    ### Summary
    + Authors: {authors_str}
    + Papers by authors: {num_papers_by_authors}
    + Number of collaborations between authors: {find_num_collaborations(df)}
    + Numer of citing papers: {num_papers_citing}
    + Average citations: {mean_cites}
    + Maximum citations: {max_cites}
    + Number of total authors: {num_authors}
    """
    return markdown


def find_num_collaborations(df):
    authors = df[df['paper_key'] == 'origin paper']['author_names'][0]
    collabs = np.zeros(df.shape[0])

    for row in df.itertuples():
        num_authors = 0
        for author in authors:
            if author in row.author_names:
                num_authors += 1
        if num_authors > 1:
            collabs[row.Index] = 1
    return int(collabs.sum())
