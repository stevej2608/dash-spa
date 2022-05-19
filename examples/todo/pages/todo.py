from dash import html, dcc, ALL
from dash import html, callback
import dash_bootstrap_components as dbc
from dash_spa import register_page, trigger_index, page_container_append, match, NOUPDATE

from dash_spa.components import ReduxStore

from .todo_model import TODO_MODEL, ModelActions as action, can_undo, can_redo

page = register_page(__name__, path='/', title="Dash Todo", short_name='Todo')

# Raw UI taken from:
# https://github.com/dsardar099/ToDoApp

Redux = ReduxStore(id=page.id('store'), data=TODO_MODEL)

class ListEntryAIO(html.Div):

    Match = match({'type': page.id('list_entry'), 'idx': ALL})

    @Redux.action(Match.input.n_clicks)
    def _delete(button_clicks):
        index = trigger_index()
        if index is not None and button_clicks[index]:
            return action.delete, index
        else:
            return NOUPDATE

    def __init__(self, entry, index, aio_id):
        id = ListEntryAIO.Match.idx(index)
        button = html.Button("Delete", id=id, className='btn btn-danger')
        super().__init__([
            button,
            html.Span(entry, className='ps-5 list-content')
            ], className='col-12 text-start list py-2 mt-1')


def activity_list():
    pfx = page.id

    def list_items(entries):
        if entries:
            return [ListEntryAIO(e, idx, pfx('list_entry'))  for idx, e in enumerate(entries)]
        else:
            return html.Div("Either you have finished all the tasks or You have not added any task",
                className='col-12 rounded text-center bg-complete h4 p-4')

    items = list_items(Redux.data['todo'])
    title = html.Div("ToDo List", className='col-12 text-center h3 bg-info text-light mb-2 p-2')
    body = html.Div(items, id=page.id('item_list'))

    @callback(body.output.children, Redux.store.input.data)
    def list_update(state):
        if state:
            return list_items(state['todo'])
        else:
            return NOUPDATE

    return html.Div([title, body], className='row justify-content-center bg-light pb-2 border border-secondary border-3 rounded shadow')

def new_activity_form():
    pfx = page.id

    input = dcc.Input(type='text', className='form-control', id=pfx('todo'), placeholder='Add ToDo', required='')
    button = dbc.Button("Add", className='btn btn-success', id=pfx('submit'))

    @Redux.action(button.input.n_clicks, input.state.value)
    def _add(button_clicks, input):
        if button_clicks and input:
            return action.add, input
        else:
             NOUPDATE

    return html.Div([
        html.Div(input, className='col-md-8 mt-2'),
        html.Div(button, className='col-2 mt-2')
    ], className='row g-3 justify-content-center mt-3 pb-4')


def undo_redo_buttons():
    pfx = page.id

    undo = dbc.Button("Undo", id=pfx('undo'), className='btn btn-info')
    redo = dbc.Button("Redo", id=pfx('redo'), className='btn btn-primary')

    @Redux.action(undo.input.n_clicks)
    def _undo(button_clicks):
        return action.undo if button_clicks else NOUPDATE

    @Redux.action(redo.input.n_clicks)
    def _redo(button_clicks):
        return action.redo if button_clicks else NOUPDATE

    @callback(undo.output.disabled, redo.output.disabled, Redux.store.input.data)
    def _disable_buttons(state):
        redo_disabled = not can_redo(state)
        undo_disabled = not can_undo(state)
        return undo_disabled, redo_disabled

    return html.Div([
        html.Div(undo, className='col-5 text-right'),
        html.Div(redo, className='col-5 text-left')
    ], className='row justify-content-center mt-5')

page_container_append(Redux)

layout = html.Div([
        html.Div([
            html.Div("To Do App", className='col-md-6 text-center h2 py-2')
        ], className='row justify-content-center mt-2 bg-warning rounded'),
        html.Div([
            html.Div([
                html.Div([
                    new_activity_form(),
                    undo_redo_buttons()
                ], className='bg-light py-5 border border-secondary border-3 rounded shadow')
            ], className='col-12 col-md-6 text-center'),
            html.Div([
                html.Div(activity_list(), className='px-3 pt-2 pt-md-0')
            ], className='col-12 col-md-6 text-center')
        ], className='row justify-content-center pt-4'),
    ], className='container')
