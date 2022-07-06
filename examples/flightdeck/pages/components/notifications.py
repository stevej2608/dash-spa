from dash import html
from dash_svg import Svg, Path
from dash_spa import register_page,  callback
from dash_spa.alert import SweetAlert
from dash_spa.logging import log
from ..icons.hero import HOME_ICON
from ..common import sideBar, mobileNavBar, topNavBar, footer

register_page(__name__, path="/pages/components/notifications.html", title="Dash/Flightdeck - Notification")

def breadCrumbs():
    return  html.Nav([
        html.Ol([
            html.Li([
                html.A([
                    HOME_ICON
                ], href='#')
            ], className='breadcrumb-item'),
            html.Li([
                html.A("Notifications", href='#')
            ], className='breadcrumb-item'),
            html.Li("Buttons", className='breadcrumb-item active', **{"aria-current": "page"})
        ], className='breadcrumb breadcrumb-dark breadcrumb-transparent')
    ], className='d-none d-md-inline-block', **{"aria-label": "breadcrumb"})


def banner():
    return html.Div([
        html.Div([
            html.H1("Notifications", className='h4'),
            html.P("Dozens of reusable components built to provide buttons, alerts, popovers, and more.", className='mb-0')
        ], className='mb-3 mb-lg-0'),
        html.Div([
            html.A([
                html.I(className='far fa-question-circle me-1'),
                "Buttons Docs"
            ], href='https://themesberg.com/docs/volt-bootstrap-5-dashboard/components/buttons/', className='btn btn-outline-gray')
        ])
    ], className='d-flex justify-content-between w-100 flex-wrap')


def DocumentationLink(href):
    return html.Div([
        html.A([
            Svg([
                Path(fillRule='evenodd', d='M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z', clipRule='evenodd')
            ], className='icon icon-xxs me-2', fill='currentColor', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg'),
            'Documentation'
        ], href=href, className='btn btn-outline-gray-500 d-inline-flex align-items-center')
    ], className='card-header border-gray-100 d-flex justify-content-between align-items-center')


def notifications_test():

    success_alert = SweetAlert(id='test', title='Success alert', text='Your work has been saved', show_confirm_button=True, timer=10000)
    btn = html.Button("Success alert", className='btn btn-success', id='successAlert')

    @callback(success_alert.output.modified_timestamp, btn.input.n_clicks_timestamp, prevent_initial_call=True)
    def alert_cb(time_stamp):
        log.info('alert_cb %s', time_stamp)
        return time_stamp

    return html.Div([success_alert, btn])


def notifications():

    return html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.H2("Sweet alerts", className='h4 mb-0'),
                        DocumentationLink('https://themesberg.com/docs/volt-bootstrap-5-dashboard/plugins/sweet-alerts/')
                    ], className='card-header border-gray-100 d-flex justify-content-between align-items-center'),
                    html.Div([
                        html.Button("Basic alert", className='btn btn-gray-800', id='basicAlert'),
                        html.Button("Info alert", className='btn btn-info', id='infoAlert'),
                        html.Button("Success alert", className='btn btn-success', id='successAlert'),
                        html.Button("Danger alert", className='btn btn-danger', id='dangerAlert'),
                        html.Button("Warning alert", className='btn btn-warning', id='warningAlert'),
                        html.Button("Question", className='btn btn-gray-200', id='questionAlert')
                    ], className='card-body')
                ], className='card border-0 shadow')
            ], className='col-12 col-lg-6'),
            html.Div([
                html.Div([
                    html.Div([
                        html.H2("Notyf", className='h4 mb-0'),
                        DocumentationLink('https://themesberg.com/docs/volt-bootstrap-5-dashboard/plugins/notifications/')
                    ], className='card-header border-gray-100 d-flex justify-content-between align-items-center'),
                    html.Div([
                        html.Button("Top left info", className='btn btn-info', id='notifyTopLeft'),
                        html.Button("Top right danger", className='btn btn-danger', id='notifyTopRight'),
                        html.Button("Bottom left warning", className='btn btn-warning', id='notifyBottomLeft'),
                        html.Button("Primary bottom right", className='btn btn-gray-800', id='notifyBottomRight')
                    ], className='card-body')
                ], className='card border-0 shadow')
            ], className='col-12 col-lg-6')
        ], className='row')


layout = html.Div([
        mobileNavBar(),
        sideBar(),
        html.Main([
            topNavBar(),
            html.Div([
                breadCrumbs(),
                banner()
            ], className='py-4'),
            notifications_test(),
            footer()
        ], className='content')
    ])
