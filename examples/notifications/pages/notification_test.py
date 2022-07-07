from dash import html
from dash_spa import register_page, NOUPDATE
from dash_spa.alert import Alert, SPA_ALERT


register_page(__name__, path='/', title="Alert Test", short_name='Alerts')

def basic_alert(title, className, id):
    btn2 = html.Button(title, className=className, id=id)

    SPA_ALERT.update(btn2.input.n_clicks, prevent_initial_call=True)
    def alert_cb(clicks, store):
        if clicks:
            alert = Alert(title, 'You clicked the button!')
            return alert.report()
        else:
            return NOUPDATE

    return btn2


def page_layout():

    btn1 = html.Button("Basic alert", className='btn btn-gray-800', id='basicAlert1')
    @SPA_ALERT.update(btn1.input.n_clicks, prevent_initial_call=True)
    def btn_cb(clicks, store):
        if clicks:
            alert = Alert("Basic alert", f'You clicked the button {clicks} times!')
            return alert.report()
        else:
            return NOUPDATE

    btn2 = html.Button("Info alert", className='btn btn-info', id='infoAlert')
    @SPA_ALERT.update(btn2.input.n_clicks, prevent_initial_call=True)
    def btn_cb(clicks, store):
        if clicks:
            alert = Alert("Info alert", f'You clicked the button {clicks} times!', 'info')
            return alert.report()
        else:
            return NOUPDATE

    btn3 = html.Button("Success alert", className='btn btn-success', id='successAlert')
    @SPA_ALERT.update(btn3.input.n_clicks, prevent_initial_call=True)
    def btn_cb(clicks, store):
        if clicks:
            alert = Alert("Success alert", 'Your work has been saved', showConfirmButton=True, timer=1500)
            return alert.report()
        else:
            return NOUPDATE

    btn4 = html.Button("Warning alert", className='btn btn-warning', id='warningAlert')
    @SPA_ALERT.update(btn4.input.n_clicks, prevent_initial_call=True)
    def btn_cb(clicks, store):
        if clicks:
            alert = Alert("Warning alert", 'Something went wrong!', icon='warning')
            return alert.report()
        else:
            return NOUPDATE

    btn5 = html.Button("Question", className='btn btn-gray-200', id='questionAlert')
    @SPA_ALERT.update(btn5.input.n_clicks, prevent_initial_call=True)
    def btn_cb(clicks, store):
        if clicks:
            alert = Alert('The Internet?', 'That thing is still around?', icon='question')
            return alert.report()
        else:
            return NOUPDATE

    # Return page layout

    WS = "\n"

    return html.Div([btn1, WS, btn2, WS, btn3, WS, btn4, WS, btn5])

layout = page_layout()
