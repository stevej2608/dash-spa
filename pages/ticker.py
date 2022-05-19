from dash import html, dcc, callback, no_update as NO_UPDATE
import dash_bootstrap_components as dbc
import colorlover as cl
import pandas as pd
from dash_spa import register_page

from pages import TICKER_SLUG

page = register_page(__name__, path=TICKER_SLUG, title="Dash Ticker", short_name='Ticker')

# https://github.com/plotly/dash-stock-tickers-demo-app
#
# The original app hs been modified adding a persistence store for the
# ticker selection.

colorscale = cl.scales['9']['qual']['Paired']

try:
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/dash-stock-ticker-demo.csv')
except Exception:
    print("Unable to read 'dash-stock-ticker-demo.csv' from github, no internet connection?")
    exit(0)


ticker_store = dcc.Store(id=page.id('current_tickers'), storage_type='session')

stock_ticker_dropdown = dcc.Dropdown(
    id=page.id('stock_ticker'),
    value="",
    options=[{'label': s[0], 'value': str(s[1])}
                for s in zip(df.Stock.unique(), df.Stock.unique())],
    multi=True,
)

graphs = html.Div(id=page.id('graphs'))

# Callback to create the charts for requested tickers

@callback(graphs.output.children, ticker_store.output.data, stock_ticker_dropdown.input.value, ticker_store.state.data)
def _update_graph(tickers, current_tickers):
    if tickers is None:
        tickers = current_tickers or []
    return update_graph(tickers), tickers

@callback(stock_ticker_dropdown.output.value, ticker_store.state.data, ticker_store.input.modified_timestamp )
def _store_cb(data, ts):
    return data if data else NO_UPDATE

layout = html.Div([
        html.H2('Finance Explorer'),
        html.Br(),
        stock_ticker_dropdown,
        html.Br(),
        graphs,
        ticker_store
    ], className="container")

def bbands(price, window_size=10, num_of_std=5):
    rolling_mean = price.rolling(window=window_size).mean()
    rolling_std = price.rolling(window=window_size).std()
    upper_band = rolling_mean + (rolling_std*num_of_std)
    lower_band = rolling_mean - (rolling_std*num_of_std)
    return rolling_mean, upper_band, lower_band

def update_graph(tickers):
    graphs = []

    if not tickers:
        graphs.append(html.H3(
            "Select a stock ticker.",
            style={'marginTop': 20, 'marginBottom': 20}
        ))
    else:
        for i, ticker in enumerate(tickers):

            dff = df[df['Stock'] == ticker]

            candlestick = {
                'x': dff['Date'],
                'open': dff['Open'],
                'high': dff['High'],
                'low': dff['Low'],
                'close': dff['Close'],
                'type': 'candlestick',
                'name': ticker,
                'legendgroup': ticker,
                'increasing': {'line': {'color': colorscale[0]}},
                'decreasing': {'line': {'color': colorscale[1]}}
            }
            bb_bands = bbands(dff.Close)
            bollinger_traces = [{
                'x': dff['Date'], 'y': y,
                'type': 'scatter', 'mode': 'lines',
                'line': {'width': 1, 'color': colorscale[(i*2) % len(colorscale)]},
                'hoverinfo': 'none',
                'legendgroup': ticker,
                'showlegend': True if i == 0 else False,
                'name': f'{ticker} - bollinger bands'
            } for i, y in enumerate(bb_bands)]
            graphs.append(dcc.Graph(
                id=ticker,
                figure={
                    'data': [candlestick] + bollinger_traces,
                    'layout': {
                        'margin': {'b': 0, 'r': 10, 'l': 60, 't': 0},
                        'legend': {'x': 0}
                    }
                }
            ))

    return graphs
