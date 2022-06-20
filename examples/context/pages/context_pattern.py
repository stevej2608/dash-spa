from dash import html
from dash_spa import prefix, register_page, NOUPDATE

from .button_toolbar import ButtonContext, button_toolbar

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

@ButtonContext.Provider(id='test')
def layout_page():

    # Changes in the ButtonContext state will force
    # layout_page() to update the UI

    def report(key, btns):
        msg = [f'{btn.id} clicks={btn.clicks}' for btn in btns]
        return html.H4(f'{key} : {", ".join(msg)}')

    pid = prefix('test')

    toolbar_1 = button_toolbar("main", ['close', "exit", 'refresh'], id=pid('main'))
    toolbar_2 = button_toolbar("page", ['next', "prev", 'top', 'bottom'], id=pid('page'))

    state = ButtonContext.getState('state')

    button_report = html.Div([
        report(key,item) for key, item in state.items()
        ], style={'background-color': '#b6b6b6'})

    title = html.H3('React.js Context Example')

    return html.Div([title, toolbar_1, toolbar_2, button_report])


layout = layout_page()
