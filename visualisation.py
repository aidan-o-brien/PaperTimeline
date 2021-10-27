import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import matplotlib
from matplotlib import cm
import numpy as np


def preprocess(df):

    # Add place holder for y axis, reset index and remove blanks for authors
    df['place_holder'] = 0
    df.reset_index(drop=True, inplace=True)
    df.replace('', float('NaN'), inplace=True)
    df.dropna(subset=['author_names'], inplace=True)

    # If there has been a paper in this month (and year), add 1 to placeholder
    # Create date column for just month and year
    df.coverDate = df.coverDate.astype('datetime64')
    df['month_year'] = pd.to_datetime(df['coverDate']).dt.to_period('M')

    # Create a dictionary of month and years
    datetime_dict = {date: 0 for date in df.month_year.unique()}

    # Loop through papers in df
    for row in df.itertuples():
        # Set the value for place_holder
        df.at[row.Index, 'place_holder'] = datetime_dict[row.month_year]
        # Add one to the value
        datetime_dict[row.month_year] += 1

    # Set date to start of month for neatness on visualisation
    df['month_year'] = df['month_year'].dt.to_timestamp()

    return df


def create_viz(df, origin_date):
    # Plot figure
    fig = px.scatter(df, x='month_year', y='place_holder', color='paper_key',
                     hover_data={'paper_key': False,
                                 'place_holder': False,
                                 'coverDate': False,
                                 'title': True})

    # Formatting
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type='date'))
    fig.update_layout(height=400, title_text='Research Timeline')
    fig.update_yaxes(visible=False)
    fig.update_layout(hovermode="closest")
    ## Add vertical line at origin paper (month but not day)
    fig.add_vline(x=origin_date.to_period('M').to_timestamp(), line_dash='dash')

    return fig


def create_cites_viz(df, origin_date):

    df['Citations'] = df['citedby_count'].astype(int)

    fig = px.scatter(df, x='month_year', y='place_holder',
                     color='Citations',
                     range_color=[0, 150],
                     hover_data={'place_holder': False,
                                 'title': True,
                                 'paper_key': False,
                                 'month_year': False},
                     symbol='paper_key')

    # Formatting
    fig.update_layout(height=400, title='Research Timeline',
                      hovermode='closest',
                      legend=dict(orientation="h", yanchor="bottom",
                                  y=1, xanchor="right", x=1))
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type='date'))
    fig.update_yaxes(visible=False)
    fig.add_vline(x=origin_date.to_period('M').to_timestamp(), line_dash='dash')

    return fig
