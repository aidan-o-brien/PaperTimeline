"""A helper file to help run the streamlit_app.py file."""

import base64
import numpy as np


def create_search_filter(data, query):
    '''Searches the title and abstract (description) of the data DataFrame
    and returns a boolean filter which is True for papers that contain the
    query term.'''

    # Search through title and abstract
    title_bool = data['title'].str.contains(query, case=False, regex=False)
    abstract_bool = data['description'].str.contains(query, case=False, regex=False)

    # Convert to np arrays for boolean logic
    title_bool = title_bool.to_numpy(dtype=bool)
    abstract_bool = abstract_bool.to_numpy(dtype=bool)

    return np.logical_or(title_bool, abstract_bool)


def create_author_filter(data, authors_filter):
    '''Searches the dataframe for each author in the authors_filter list,
    which has come direct from user input. Returns an array for slicing
    the dataframe.'''

    temp_df = data.explode('author_names')

    # for each author, filter df for just their papers
    indices = []
    for author in authors_filter:
        author_indices = temp_df[temp_df['author_names'] == author].index.to_numpy()
        for idx in author_indices:
            indices.append(idx)
    # We only care about unique papers, no duplicates
    indices = set(indices)
    index_array = np.zeros(data.shape[0], dtype=bool)
    for idx in indices:
        index_array[idx] = 1

    return index_array


def get_table_download_link(data):
    '''Takes a data frame and returns html to download csv file.
    Source: https://discuss.streamlit.io/t/export-and-download-dataframe-to-
    csv-file/9926.'''

    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="research_timeline\
            .csv">Download data</a>'
    return href


def produce_sum_stats(data):
    '''Produces some summary statistics for the dataframe. Summary statistics
    are returned in markdown form.'''

    origin_paper = data[data['paper_key'] == 'origin paper']
    # authors
    authors = origin_paper['author_names'][0]
    authors_str = ''
    for i, name in enumerate(authors):
        if i == len(authors) - 1:
            authors_str += name
        else:
            authors_str += f'{name}; '
    num_papers_by_authors = data[data['paper_key'] == 'papers by authors'].shape[0]
    num_papers_citing = data[data['paper_key'] == 'citing papers'].shape[0]
    cites = data['citedby_count'].to_numpy(dtype=np.float)
    mean_cites = cites.mean()
    max_cites = cites.max()
    temp_df = data.explode('author_names')
    num_authors = len(temp_df.author_names.unique())

    markdown = f"""
    ### Summary
    + Authors: {authors_str}
    + Papers by authors: {num_papers_by_authors}
    + Number of collaborations between authors: {find_num_collaborations(data)}
    + Numer of citing papers: {num_papers_citing}
    + Average citations: {mean_cites:.2f}
    + Maximum citations: {int(max_cites)}
    + Number of total authors: {num_authors}
    """

    return markdown


def find_num_collaborations(data):
    '''Finds the number of papers where the authors of the origin paper
    have collaborated.'''

    authors = data[data['paper_key'] == 'origin paper']['author_names'][0]
    collabs = np.zeros(data.shape[0])

    for row in data.itertuples():
        num_authors = 0
        for author in authors:
            if author in row.author_names:
                num_authors += 1
        if num_authors > 1:
            collabs[row.Index] = 1

    return int(collabs.sum())
