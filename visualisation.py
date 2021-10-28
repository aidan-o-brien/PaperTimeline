"""File for preprocessing and visualisation of data."""

import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def preprocess(df):
    '''Conduct the following preprocessing on data:
    - Add placeholder variable for y axis separability
    - Remove duplicates and blanks
    - Align papers in the same month for aesthetics.'''

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


def create_cites_viz(df, origin_date):
    '''Create a visualisation of the data provided - possibly filtered by
    user input. Regardless of filtered data provided, visualisation has a
    dashed line where the origin paper is.'''

    # Cast citations as integer, instead of string for color scale
    df = df.copy()
    df['Citations'] = df['citedby_count'].astype(int)

    # Create figure
    fig = px.scatter(df, x='month_year', y='place_holder',
                     color='Citations',
                     color_continuous_scale='Plasma_r',
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


def create_wordcloud(df):
    '''Create a wordcloud from the abstract of papers provided.'''

    # Consolidate all abstracts into one string
    text = ''
    for abstract in df.description:
        if isinstance(abstract, str):
            text += abstract

    # Create word cloud
    wordcloud = WordCloud(max_words=40,
                          background_color='white').generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')

    return fig
