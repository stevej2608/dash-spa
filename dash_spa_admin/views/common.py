from enum import IntEnum
from collections import namedtuple
import re
from dash import html

class USER(IntEnum):
    NONE = 0
    USER_ALLREADY_EXISTS = 1
    EMAIL_SENT = 2
    VALIDATED = 3
    VALIDATION_FAILED = 4

LOGIN_ENDPOINT = 'login'
LOGOUT_ENDPOINT = 'logout'

REGISTER_ENDPOINT = 'register'
REGISTER_ADMIN_ENDPOINT = 'register_admin'
REGISTER_VERIFY_ENDPOINT = 'register_verify'

FORGOT_ENDPOINT = 'forgot'
FORGOT_CODE_ENDPOINT = 'forgotcode'
FORGOT_PASSWORD_ENDPOINT = 'forgotpassword'

USERS_ENDPOINT = 'users'

def form_values(dt):
    obj = namedtuple("FormFields", dt.keys())(*dt.values())
    return obj

def email_valid(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

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
