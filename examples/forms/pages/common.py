from dash import html, dcc

def form_container(title, form):
    return html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H4(title, className="card-title"),
                    form,
                ], className='card-body')
            ], className="card fat")
        ], className="col-6 mx-auto")
    ], className="row align-items-center h-100")

store = dcc.Store(id='user_details', storage_type='session')
