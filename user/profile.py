import dash_html_components as html
from .user import blueprint as spa

from flask_login import current_user


def big_center(text):
    return html.H2(text, className='display-3 text-center')

@spa.route('/profile', title='User')
def profile():

    if current_user and not current_user.is_anonymous:
        name = current_user.name
    else:
        name = 'Guest'

    return html.Header([
        big_center("Dash/SPA Welcomes"),
        big_center(name)
    ], className='jumbotron my-4')
