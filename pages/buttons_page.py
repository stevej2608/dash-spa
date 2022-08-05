from dash import html
from dash_spa import register_page
from dash_spa.logging import log

from pages import BUTTONS_PAGE_SLUG

from .buttons.button_toolbar import ToolbarContext, button_toolbar, TBState

page = register_page(__name__, path=BUTTONS_PAGE_SLUG, title="Button Toolbar Page", short_name='Buttons')

# Example of using the Dash/SPA context pattern
# that allows a components state change to be easily passed
# between components and trigger UI updates.
#
# The example creates two panels, each with two instances of
# a toolbar component. The buttons in each toolbar update the common
# ButtonContext for the panel. Because the layout_page() method
# is decorated with ButtonContext.Provider it  will be
# called to refresh the UI whenever the context changes.


def tb_report(tb: TBState):
    """reports single toolbar state"""

    msg = [f'{btn.name}={btn.clicks}' for btn in tb.buttons]
    return html.H4(f'{tb.title}: {", ".join(msg)}')

@ToolbarContext.Provider()
def top_panel_layout():

    log.info('top_panel_layout()')

    # Create some toolbars

    main_toolbar = button_toolbar(page.id("top_main"), TBState("main", ['close', "exit", 'refresh']))
    page_toolbar = button_toolbar(page.id("top_page"), TBState("page", ['next', "prev", 'top', 'bottom']))

    state = ToolbarContext.getState()

    title = html.H3('Toolbar Component Example (with persistent state)')

    report = html.Div([tb_report(tb) for tb in state.items()], style={'background-color': '#e6e6e6'})
    report.children.insert(0, html.H3('Toolbar Report'))

    return html.Div([title, main_toolbar, page_toolbar, report])


@ToolbarContext.Provider(persistent=False)
def bottom_panel_layout():

    log.info('bottom_panel_layout()')

    # Create some toolbars

    main_toolbar = button_toolbar(page.id("bottom_main"), TBState("main", ['close', "exit", 'refresh']))
    page_toolbar = button_toolbar(page.id("bottom_page"), TBState("page", ['next', "prev", 'top', 'bottom']))

    state = ToolbarContext.getState()

    title = html.H3('Toolbar Component Example (without persistent state)')

    report = html.Div([tb_report(tb) for tb in state.items()], style={'background-color': '#e6e6e6'})
    report.children.insert(0, html.H3('Toolbar Report'))


    return html.Div([title, main_toolbar, page_toolbar, report])

def layout():
    log.info('layout()')
    top = top_panel_layout()
    bottom = bottom_panel_layout()
    return html.Div([top, bottom])
