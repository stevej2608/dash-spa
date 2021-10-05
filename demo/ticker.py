from holoniq.utils import log
import colorlover as cl

from dash import html, dcc
import pandas as pd
from dash_spa import SpaComponents

from .demo import blueprint as demo

# Taken from Dash example, see:
# https://github.com/plotly/dash-stock-tickers-demo-app

current_tickers = []

colorscale = cl.scales['9']['qual']['Paired']

try:
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/dash-stock-ticker-demo.csv')
except Exception:
    print("Unable to read 'dash-stock-ticker-demo.csv' from github, no internet connection?")
    exit(0)


@demo.route('/ticker', title='Ticker')
def ticker(ctx):
    spa = demo.get_spa('ticker')

    log.info('/ticker')

    # http://localhost:8050/finance_explorer?tickers=TSLA

    querystring_name = 'tickers'

    stock_ticker_dropdown = spa.Dropdown(
        id='stock_ticker',
        value=ctx.get_url_query_values(querystring_name),
        name=querystring_name,
        options=[{'label': s[0], 'value': str(s[1])}
                 for s in zip(df.Stock.unique(), df.Stock.unique())],
        multi=True,
    )

    graphs = spa.Div(id='graphs')

    # Callback to create the charts for requested tickers

    @spa.callback(graphs.output.children, [stock_ticker_dropdown.input.value])
    def _update_graph(tickers):
        global current_tickers
        log.info('_update_graph, stock_ticker_dropdown.input: %s', tickers)
        if tickers is None:
            tickers = current_tickers
        current_tickers = tickers
        return update_graph(tickers)


    # Callback to update the browser search-bar with the
    # selected tickers

    location = spa.Redirect(id='redirect', refresh=False)

    @spa.callback(location.output.href, [stock_ticker_dropdown.input.value])
    def _update_url(tickers):
        log.info('_update_url, stock_ticker_dropdown.input: %s', tickers)
        href = SpaComponents.NOUPDATE
        if tickers is not None:
            href = demo.url_for('ticker')
            urlargs = '+'.join(tickers)
            search = f'?{querystring_name}={urlargs}'
            href += search
        return href


    # Layout the page

    return html.Div([
        location,
        html.H2('Finance Explorer'),
        html.Br(),
        stock_ticker_dropdown,
        html.Br(),
        graphs
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
