import dash
from dash import Dash, html, no_update as NOUPDATE
import dash_bootstrap_components as dbc
from dash import html, callback

from dash_spa import prefix, logging
from dash_spa.logging import log

from dash_spa.utils import DashLogger, DEBUG_LEVEL
from server import serve_app

from dash_spa.components.redux_store import ReduxStore

pfx = prefix("redux_test")

Redux = ReduxStore(id=pfx('store'), storage_type='session',
        data = {
            "btn1" : 0,
            "btn2" : 0,
            }
        )

def layout():
    btn1 = html.Button("Button 1", id=pfx('btn1'))
    btn2 = html.Button("Button 2", id=pfx('btn2'))
    container = html.Div(id=pfx('container'))

    @Redux.update(btn1.input.n_clicks)
    def btn1_update(clicks, store):
        if clicks:
            log.info('Btn 1 clicked %d (%s)', clicks, store)
            store['btn1'] += 1
            return store
        return NOUPDATE

    @Redux.update(btn2.input.n_clicks)
    def btn2_update(clicks, store):
        if clicks:
            log.info('Btn 2 clicked %d (%s)', clicks, store)
            store['btn2'] += 1
            return store
        return NOUPDATE

    @callback(container.output.children, Redux.store.input.data)
    def container_update(store):
        if store:
            return f"Btn 1 clicked {store['btn1']} times, Btn 2 clicked {store['btn2']} times"
        return NOUPDATE

    return html.Div([btn1, btn2, container])

def create_dash():
    app = dash.Dash( __name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    return app


def create_app(dash_factory) -> Dash:

    content = layout()

    _layout = html.Div([
            Redux,
            html.Div([
                html.Div([
                    html.Div([], className="col-md-1"),
                    html.Div(content, id='page-content', className="col-md-10"),
                    html.Div([], className="col-md-1")
                ], className='row')
            ], className="container-fluid"),
        ])

    app = dash_factory()
    app.layout = _layout
    return app

# python -m examples.todo.redux_test

if __name__ == "__main__":
    logging.setLevel("INFO")
    app = create_app(create_dash)
    #logger = DashLogger(DEBUG_LEVEL.VERBOSE)
    serve_app(app, debug=False)


