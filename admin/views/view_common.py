from dash import html
from dash_spa import Blueprint

blueprint = Blueprint('admin')

def form_layout(title, form):
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
