from dash import html, dcc
import dash_holoniq_components as dhc
from dash_spa import NOUPDATE, callback
from dash_spa.logging import log
from dash_spa import session_context, SessionContext, dataclass
from dash_spa.spa_location import store
from dash_spa import register_page
import colorlover as cl
import pandas as pd

from pages import TICKER_SLUG

page = register_page(__name__, path=TICKER_SLUG, title="Dash Ticker", short_name='Ticker')

@dataclass
class TickerState(SessionContext):
    tickers: str = ""

# https://github.com/plotly/dash-stock-tickers-demo-app
#
# The original app hs been modified adding a session store for the
# ticker selection.

colorscale = cl.scales['9']['qual']['Paired']

try:
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/dash-stock-ticker-demo.csv')
except Exception:
    print("Unable to read 'dash-stock-ticker-demo.csv' from github, no internet connection?")
    exit(0)


def bbands(price, window_size=10, num_of_std=5):
    rolling_mean = price.rolling(window=window_size).mean()
    rolling_std = price.rolling(window=window_size).std()
    upper_band = rolling_mean + (rolling_std*num_of_std)
    lower_band = rolling_mean - (rolling_std*num_of_std)
    return rolling_mean, upper_band, lower_band

def update_graph(tickers=[]):
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

            graphs.append(html.Br())

    return html.Div(graphs)

# http://default:5026/ticker?tickers=TSLA+GOOGL

def layout(tickers: str = None) -> html.Div:
    """Layout the tickers page

    Args:
        tickers (str, optional): querystring tickers to be displayed. Defaults to None.

    Returns:
        html.Div: Ticker page markup
    """

    tickers = tickers.split(' ') if tickers is not None else []

    ctx = session_context(TickerState)
    ctx.tickers = tickers

    #location = dhc.Location(id='ticker_loc', refresh=True)

    ticker_dropdown = dcc.Dropdown(
        id=page.id('stock_ticker'),
        value=tickers,
        options=[{'label': s[0], 'value': str(s[1])}
                    for s in zip(df.Stock.unique(), df.Stock.unique())],
        multi=True)

    # Update the the location bar with the querystring values selected by the
    # drop-down. This will cause a page refresh

    @store.update(ticker_dropdown.input.value, prevent_initial_callback=True)
    def _update_loc(value, store):
        ctx = session_context(TickerState)
        try:
            if value != ctx.tickers:
                ctx.tickers = value
                href = f"{page.path}?tickers={'+'.join(value)}"
                log.info('href=%s', href)
                return href
        except Exception:
            pass

        return NOUPDATE

    graphs = update_graph(tickers)
    graph_container = html.Div(graphs, id='graphs')

    return html.Div([
        html.H2('Finance Explorer'),
        html.Br(),
        ticker_dropdown,
        html.Br(),
        graph_container
    ], className="container")