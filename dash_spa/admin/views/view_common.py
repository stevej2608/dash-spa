from collections import namedtuple
from dash import html

from dash_spa import Blueprint
from dash_spa.admin.exceptions import InvalidAccess

blueprint = Blueprint('admin')

def form_values(dt):
    obj = namedtuple("FormFields", dt.keys())(*dt.values())
    return obj

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

def validate_user(ctx):
    login_manager = ctx.login_manager
    if login_manager.isAdmin():
        return True
    raise InvalidAccess("Must be signed in as admin")
