from dash import html
from dash_spa import register_page
from dash_spa.spa_context import createContext, ContextState, dataclass
from dash_spa.logging import log

page = register_page(__name__, path='/', title="Button Test", short_name='Buttons')

@dataclass
class ButtonState(ContextState):
    clicks: int = 1000

ButtonContext = createContext(ButtonState)

@ButtonContext.Provider()
def page_layout():
    log.info('page_layout()')

    state = ButtonContext.getState()
    btn = html.Button("Button", id='btn')

    @ButtonContext.On(btn.input.n_clicks)
    def btn_click(clicks):
        log.info('btn_click()')
        state.clicks += 1

    div = html.Div(f"Button pressed {state.clicks} times!", id='div')

    return html.Div([btn, div])

layout = page_layout
