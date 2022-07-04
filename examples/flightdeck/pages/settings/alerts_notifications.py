from dash import html, dcc


def alertsNotifications():
    return  html.Div([
        html.H2("Alerts & Notifications", className='h5 mb-4'),
        html.Ul([
            html.Li([
                html.Div([
                    html.H3("Company News", className='h6 mb-1'),
                    html.P("Get Rocket news, announcements, and product updates", className='small pe-4')
                ]),
                html.Div([
                    html.Div([
                        dcc.Input(className='form-check-input', type='checkbox', id='user-notification-1'),
                        html.Label(className='form-check-label', htmlFor='user-notification-1')
                    ], className='form-check form-switch')
                ])
            ], className='list-group-item d-flex align-items-center justify-content-between px-0 border-bottom'),
            html.Li([
                html.Div([
                    html.H3("Account Activity", className='h6 mb-1'),
                    html.P("Get important notifications about you or activity you've missed", className='small pe-4')
                ]),
                html.Div([
                    html.Div([
                        dcc.Input(className='form-check-input', type='checkbox', id='user-notification-2', value=False),
                        html.Label(className='form-check-label', htmlFor='user-notification-2')
                    ], className='form-check form-switch')
                ])
            ], className='list-group-item d-flex align-items-center justify-content-between px-0 border-bottom'),
            html.Li([
                html.Div([
                    html.H3("Meetups Near You", className='h6 mb-1'),
                    html.P("Get an email when a Dribbble Meetup is posted close to my location", className='small pe-4')
                ]),
                html.Div([
                    html.Div([
                        dcc.Input(className='form-check-input', type='checkbox', id='user-notification-3', value=False),
                        html.Label(className='form-check-label', htmlFor='user-notification-3')
                    ], className='form-check form-switch')
                ])
            ], className='list-group-item d-flex align-items-center justify-content-between px-0')
        ], className='list-group list-group-flush')
    ], className='card card-body border-0 shadow mb-4 mb-xl-0')
