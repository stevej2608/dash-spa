from dash import html, get_asset_url
import dash_spa as spa

# Python/Dash clone of node.js project template that's normally created using Create React App (CRA)

spa.register_page(__name__, path='', title="Dash CRA Example")

def layout():
    return html.Div([
    html.Header([
        html.Img(src=get_asset_url("logo.svg"), className="App-logo", alt="logo"),
        html.P(["Edit ", html.Code("usage.py"), " and save to reload."]),
        html.A("Learn Dash", className="App-link", href="https://dash.plotly.com/",  target="_blank", rel="noopener noreferrer")
    ], className="App-header")
], className="App")
