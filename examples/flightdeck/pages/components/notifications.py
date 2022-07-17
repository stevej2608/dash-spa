from dash import html
from dash_spa import register_page, NOUPDATE
from dash_spa.alert import Alert, SPA_ALERT
from dash_spa.notyf import Notyf, SPA_NOTIFY

from ..common import breadCrumbs, banner, topNavBar, footer
from ..icons import ICON

register_page(__name__, path="/pages/components/notifications", title="Dash/Flightdeck - Notification")


def DocumentationLink(href):
    return html.Div([
        html.A([ICON.QUESTION_MARK,'Documentation'
        ], href=href, className='btn btn-outline-gray-500 d-inline-flex align-items-center')
    ], className='card-header border-gray-100 d-flex justify-content-between align-items-center')


def alert_buttons():

    btn1 = html.Button("Basic alert", className='btn btn-gray-800', id='basicAlert1')
    @SPA_ALERT.update(btn1.input.n_clicks)
    def btn_cb(clicks, store):
        if clicks:
            alert = Alert("Basic alert", f'You clicked the button {clicks} times!')
            return alert.report()
        else:
            return NOUPDATE

    btn2 = html.Button("Info alert", className='btn btn-info', id='infoAlert')
    @SPA_ALERT.update(btn2.input.n_clicks)
    def btn_cb(clicks, store):
        if clicks:
            alert = Alert("Info alert", f'You clicked the button {clicks} times!', 'info')
            return alert.report()
        else:
            return NOUPDATE

    btn3 = html.Button("Success alert", className='btn btn-success', id='successAlert')
    @SPA_ALERT.update(btn3.input.n_clicks)
    def btn_cb(clicks, store):
        if clicks:
            alert = Alert("Success alert", 'Your work has been saved', showConfirmButton=True, timer=1500)
            return alert.report()
        else:
            return NOUPDATE

    btn4 = html.Button("Warning alert", className='btn btn-warning', id='warningAlert')
    @SPA_ALERT.update(btn4.input.n_clicks)
    def btn_cb(clicks, store):
        if clicks:
            alert = Alert("Warning alert", 'Something went wrong!', icon='warning')
            return alert.report()
        else:
            return NOUPDATE

    btn5 = html.Button("Question", className='btn btn-gray-200', id='questionAlert')
    @SPA_ALERT.update(btn5.input.n_clicks)
    def btn_cb(clicks, store):
        if clicks:
            alert = Alert('The Internet?', 'That thing is still around?', icon='question')
            return alert.report()
        else:
            return NOUPDATE

    # Return page layout

    WS = "\n"

    return [btn1, WS, btn2, WS, btn3, WS, btn4, WS, btn5]


def notyf_buttons():

    btn1 = html.Button("Top left info", className='btn btn-info', id='notifyTopLeft')
    @SPA_NOTIFY.update(btn1.input.n_clicks)
    def btn_cb(clicks, store):
        if clicks:
            notyf = Notyf(message='Send us <b>an email</b> to get support')
            return notyf.report()
        else:
            return NOUPDATE

    btn2 = html.Button("Top right danger", className='btn btn-danger', id='notifyTopRight')
    @SPA_NOTIFY.update(btn2.input.n_clicks)
    def btn_cb(clicks, store):
        if clicks:
            notyf = Notyf(message='This action is not allowed.', type='error')
            return notyf.report()
        else:
            return NOUPDATE

    btn3 = html.Button("Bottom left warning", className='btn btn-warning', id='notifyBottomLeft')
    @SPA_NOTIFY.update(btn3.input.n_clicks)
    def btn_cb(clicks, store):
        if clicks:
            notyf = Notyf(message='This might be dangerous.', type='warning')
            return notyf.report()
        else:
            return NOUPDATE

    btn4 = html.Button("Primary bottom right", className='btn btn-gray-800', id='notifyBottomRight')
    @SPA_NOTIFY.update(btn4.input.n_clicks)
    def btn_cb(clicks, store):
        if clicks:
            notyf = Notyf(message='John Garreth: Are you ready for the presentation?', type='info')
            return notyf.report()
        else:
            return NOUPDATE

    # Return page layout

    WS = "\n"

    return html.Div([btn1, WS, btn2, WS, btn3, WS, btn4, WS, ])


def notifications():

    return html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.H2("Sweet alerts", className='h4 mb-0'),
                        DocumentationLink('https://themesberg.com/docs/volt-bootstrap-5-dashboard/plugins/sweet-alerts/')
                    ], className='card-header border-gray-100 d-flex justify-content-between align-items-center'),
                    html.Div(alert_buttons(), className='card-body')
                ], className='card border-0 shadow')
            ], className='col-12 col-lg-6'),
            html.Div([
                html.Div([
                    html.Div([
                        html.H2("Notyf", className='h4 mb-0'),
                        DocumentationLink('https://themesberg.com/docs/volt-bootstrap-5-dashboard/plugins/notifications/')
                    ], className='card-header border-gray-100 d-flex justify-content-between align-items-center'),
                    html.Div(notyf_buttons(), className='card-body')
                ], className='card border-0 shadow')
            ], className='col-12 col-lg-6')
        ], className='row')


layout = html.Main([
        topNavBar(),
        html.Div([
            breadCrumbs(['components', 'Notifications']),
            banner("Notifications", 'https://themesberg.com/docs/volt-bootstrap-5-dashboard/components/buttons/')
        ], className='py-4'),
        notifications(),
        footer()
    ], className='content')
