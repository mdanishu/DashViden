import dash
from dash import html, dcc, Input, Output
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import plotly.express as px

# Initialize the Dash app
app = dash.Dash(__name__)

# Read the CSV file
hist_df = pd.read_csv('Stock_History.csv')
hist_df['Date'] = pd.to_datetime(hist_df['Date'])  # Ensure Date is datetime
tickers = hist_df['Ticker'].unique()

# App layout
app.layout = html.Div([
    html.H1("Stock Data Visualization"),
    dcc.Dropdown(
        id='ticker-dropdown',
        options=[{'label': ticker, 'value': ticker} for ticker in tickers],
        value=tickers[0]  # Default value
    ),
    dcc.Dropdown(
        id='time-dropdown',
        options=[
            {'label': '3 months', 'value': '3 months'},
            {'label': '6 months', 'value': '6 months'},
            {'label': '1 year', 'value': '1 year'},
            {'label': '5 years', 'value': '5 years'},
            {'label': 'All time', 'value': 'All time'}
        ],
        value='All time'  # Default value
    ),
    dcc.Graph(id='stock-graph')
])

# Callback to update graph based on dropdowns
@app.callback(
    Output('stock-graph', 'figure'),
    [Input('ticker-dropdown', 'value'),
     Input('time-dropdown', 'value')]
)
def update_graph(selected_ticker, selected_time):
    filtered_df = hist_df[hist_df['Ticker'] == selected_ticker]

    if selected_time != 'All time':
        end_date = filtered_df['Date'].max()
        start_date = {
            '3 months': end_date - timedelta(days=90),
            '6 months': end_date - timedelta(days=180),
            '1 year': end_date - timedelta(days=365),
            '5 years': end_date - timedelta(days=365 * 5)
        }[selected_time]
        filtered_df = filtered_df[filtered_df['Date'] >= start_date]

    fig = px.line(filtered_df, x='Date', y='Price', title=f'Stock Prices for {selected_ticker}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
