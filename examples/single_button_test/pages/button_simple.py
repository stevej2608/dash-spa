from dash import html
from dash_spa import register_page, callback

page = register_page(__name__, path='/', title="Button Test", short_name='Buttons')

def page_layout():
    btn = html.Button("Button1", id=page.pfx('btn'))
    h2 = html.H2("", id=page.pfx('h2'))

    @callback(h2.output.children, btn.input.n_clicks, prevent_initial_call=True)
    def btn_cb(clicks):
        return f"Button clicked {clicks} times!"
    return html.Div([btn, h2])


layout = page_layout
