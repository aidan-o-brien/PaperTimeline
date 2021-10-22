import pandas as pd
import numpy as np


def update_bool(df, search_query):

    # Search through title and abstract
    title_bool = df['title'].str.contains(search_query, case=False, regex=False)
    abstract_bool = df['description'].str.contains(search_query, case=False, regex=False)

    # Convert to np arrays for boolean logic
    title_bool = title_bool.to_numpy(dtype=bool)
    abstract_bool = abstract_bool.to_numpy(dtype=bool)

    return np.logical_or(title_bool, abstract_bool)
