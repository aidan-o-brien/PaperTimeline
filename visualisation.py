import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def preprocess(df):
    # Cast pub_date as datetime dtype
    df.coverDate = df.coverDate.astype('datetime64')

    # Add place holder for y axis
    df['place_holder'] = 0

    # If there has been a paper in this month (and year), add 1 to placeholder
    # Convert coverDate to month and years only
    df['month_year'] = pd.to_datetime(df['coverDate']).dt.to_period('M')

    # Create a dictionary of month and years
    datetime_dict = {date: 0 for date in df.month_year.unique()}

    # Loop through papers in df
    for row in df.itertuples():
        # Set the value for place_holder
        datetime = row.month_year
        df.iat[row.Index, -2] = datetime_dict[datetime]
        # Add one to the value
        datetime_dict[datetime] += 1

    return df


def create_viz(df):
    # Plot figure
    fig = px.scatter(df, x='coverDate', y='place_holder', color='paper_key',
                     hover_data={'paper_key': False,
                                 'place_holder': False,
                                 'coverDate': False,
                                 'title': True,
                                 'eid': True})

    # Add range slider
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type='date'))

    # Formatting
    fig.update_layout(height=400, title_text='Research Timeline')
    fig.update_yaxes(visible=False)
    fig.update_layout(hovermode="x unified")
    ## Add vertical line at origin paper
    #origin_date = df[df['paper_key'] == 'origin paper']['coverDate'][0]
    #fig.add_vline(x=origin_date, line_dash='dash')

    return fig
