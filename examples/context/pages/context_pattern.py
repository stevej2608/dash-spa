from typing import List
from dash import html
from dash_spa import prefix, register_page, NOUPDATE
from dash_spa.logging import log
from dash_spa.spa_context import  ContextState, createContext, dataclass, EMPTY_LIST

from .button_toolbar import button_toolbar, TBState

register_page(__name__, path='/', title="React Pattern", short_name='React')

# Example of using the Dash/SPA React.Js style context pattern
# that allows a components state change to be easily passed
# between components and trigger UI updates.
#
# The example creates two instances of a toolbar
# component. The buttons in each toolbar update the common
# ButtonContext. Because the layout_page() method
# is decorated with ButtonContext.Provider it  will be
# called to refresh the UI whenever the context changes.

@dataclass
class ToolbarList(ContextState):
    toolbar: List[TBState] = EMPTY_LIST

TestContext = createContext(ToolbarList)

@TestContext.Provider(id='test')
def layout_page():

    tb1 = TBState("main", ['close', "exit", 'refresh'])
    tb2 = TBState("page", ['next', "prev", 'top', 'bottom'])

    state, _ = TestContext.useState(initial_state=ToolbarList([tb1, tb2]))

    log.info('state.cid=%s', state.cid)

    # Changes in the ButtonContext state will force
    # layout_page() to update the UI

    def report(tb: TBState):
        msg = [f'{btn.name} clicks={btn.clicks}' for btn in tb.buttons]
        return html.H4(f'{tb.title} : {", ".join(msg)}')

    pid = prefix('test')

    toolbar_1 = button_toolbar(TestContext, state.toolbar[0], id=pid('main'))
    toolbar_2 = button_toolbar(TestContext, state.toolbar[1], id=pid('page'))

    button_report = html.Div([
        report(tb) for tb in state.toolbar
        ], style={'background-color': '#b6b6b6'})

    title = html.H3('React.js Context Example')

    return html.Div([title, toolbar_1, toolbar_2, button_report])


layout = layout_page()
