from dash import html
from dash_spa import register_page
from dash_spa.logging import log

from .button_toolbar import ToolbarContext, button_toolbar, TBState

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


def tb_report(tb: TBState):
    """reports single toolbar state"""

    msg = [f'{btn.name}={btn.clicks}' for btn in tb.buttons]
    return html.H4(f'{tb.title} : {", ".join(msg)}')

@ToolbarContext.Provider(id='test')
def layout():

    log.info('layout_page()')

    # Create some toolbars

    main_toolbar = button_toolbar("main", TBState("main", ['close', "exit", 'refresh']))
    page_toolbar = button_toolbar("page", TBState("page", ['next', "prev", 'top', 'bottom']))

    state = ToolbarContext.getState()

    report = html.Div([tb_report(tb) for tb in state.items()], style={'background-color': '#e6e6e6'})
    report.children.insert(0, html.H3('Toolbar Report'))

    title = html.H3('Toolbar Component Example')

    return html.Div([title, main_toolbar, page_toolbar, report])

