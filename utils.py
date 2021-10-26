import pandas as pd
import numpy as np


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
    #temp_df['month_year'] = df['month_year'].astype('object')

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

    print(index_array)
    print(index_array[0])

    return index_array