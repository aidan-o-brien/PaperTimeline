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
    href = f'<a href="data:file/csv;base64,{b64}" download="research_timeline.csv">Download csv file</a>'
    return href
