import dash
from dash import Dash, html, dcc, no_update as NOUPDATE
import dash_bootstrap_components as dbc
from dash import html, callback
from dash_spa import prefix, logging
from dash_spa.logging import log

from dash_spa.utils import DashLogger, DEBUG_LEVEL
from server import serve_app

from dash_spa.components import ReduxStore

pfx = prefix('todo')

# Raw UI taken from:
# https://github.com/dsardar099/ToDoApp

Redux = ReduxStore(id=pfx('store'),
        data = {
            "action" : None,
            "todo": ["Have Tea", "Read Book", "Go to bed"]
            }
        )

class ListEntryAIO(html.Div):

    def __init__(self, entry, index, aio_id):
        pfx = prefix(aio_id)

        button = html.Button("Delete", id=pfx(index), className='btn btn-danger')

        @Redux.update(button.input.n_clicks)
        def delete_activity(button_clicks, data):
            log.info("delete_activity")
            if button_clicks:
                log.info("delete activity %s", index)
                data['action'] = f"DELETE {index}"
                return data

            return NOUPDATE

        super().__init__(html.Div([
            button,
            html.Span(entry, className='ps-5 list-content')
            ], className='col-12 text-start list py-2 mt-1'))


def activity_list():

    log.info('activity_list')

    def list_items(entries):
        if entries:
            return [ListEntryAIO(e, idx, pfx('list_entry'))  for idx, e in enumerate(entries)]
        else:
            return html.Div("Either you have finished all the tasks or You have not added any task",
                className='col-12 rounded text-center bg-complete h4 p-4')

    #items = list_items(Redux.data['todo'])

    title = html.Div("ToDo List", className='col-12 text-center h3 bg-info text-light mb-2 p-2')
    body = html.Div(id=pfx('item_list'))

    @callback(body.output.children, Redux.input.data)
    def list_update(state):
        if state:
            log.info('list_update %s', state)
            return list_items(state['todo'])
        else:
            return NOUPDATE

    return html.Div([title, body], className='row justify-content-center bg-light pb-2 border border-secondary border-3 rounded shadow')

def activity_form():
    input = dcc.Input(type='text', className='form-control', id=pfx('todo'), placeholder='Add ToDo', required='')
    button = dbc.Button("Add", className='btn btn-success', id=pfx('submit'))


    @Redux.update(button.input.n_clicks, input.state.value)
    def add_activity(button_clicks, input, state):
        if button_clicks and input:
            log.info('Input action %s', state)
            state['action'] = "todo/input"
            state['todo'].append(input)
        return state


    return html.Div([
        html.Div(input, className='col-md-8 mt-2'),
        html.Div(button, className='col-2 mt-2')
    ], className='row g-3 justify-content-center mt-3 pb-4')


def undo_redo():
    return html.Div([
        html.Div([
            dbc.Button("Undo", className='btn btn-info')
        ], className='col-5 text-right'),
        html.Div([
            dbc.Button("Redo", className='btn btn-primary')
        ], className='col-5 text-left')
    ], className='row justify-content-center mt-5')


def layout():
    return html.Div([
        html.Div([
            html.Div("To Do App", className='col-md-6 text-center h2 py-2')
        ], className='row justify-content-center mt-2 bg-warning rounded'),
        html.Div([
            html.Div([
                html.Div([
                    activity_form(),
                    undo_redo()
                ], className='bg-light py-5 border border-secondary border-3 rounded shadow')
            ], className='col-12 col-md-6 text-center'),
            html.Div([
                html.Div(activity_list(), className='px-3 pt-2 pt-md-0')
            ], className='col-12 col-md-6 text-center')
        ], className='row justify-content-center pt-4'),
    ], className='container')


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


# python -m examples.todo.todo_test

if __name__ == "__main__":
    logging.setLevel("INFO")
    app = create_app(create_dash)
    #logger = DashLogger(DEBUG_LEVEL.VERBOSE)
    serve_app(app, debug=False)