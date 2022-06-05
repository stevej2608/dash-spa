from dash import html, callback
from dash_spa import prefix, register_page, NOUPDATE
from dash_spa.logging import log
from dash_spa.spa_context import createContext, useContext

from .button_toolbar import ButtonContext, button_toolbar

register_page(__name__, path='/', title="React Pattern", short_name='React')

@ButtonContext.Provider(id='test')
def layout_page():

    def report(key, btns):
        msg = [f'{btn.id} clicks={btn.clicks}' for btn in btns]
        return html.H4(f'{key} : {", ".join(msg)}')

    pid = prefix('test')

    toolbar_1 = button_toolbar("main", ['close', "exit", 'refresh'], id=pid('main'))
    toolbar_2 = button_toolbar("page", ['next', "prev", 'top', 'bottom'], id=pid('page'))

    state = ButtonContext.getState()

    button_report = html.Div([
        report(key,item) for key, item in state.items()
        ], style={'background-color': '#b6b6b6'})

    title = html.H3('React.js Context Example')

    return html.Div([title, toolbar_1, toolbar_2, button_report])


layout = layout_page()
