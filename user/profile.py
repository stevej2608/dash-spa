from dash import html
from flask_login import current_user

from .user import blueprint as user
from dash_spa import SpaComponents

@user.route('/profile', title='User')
def profile():
    spa = user.get_spa()

    def big_center(text, id=None):
        return spa.H2(text, id=id, className='display-3 text-center')

    def page_content():
        if current_user and not current_user.is_anonymous:
            name = current_user.name
        else:
            name = 'Guest'

        return html.Header([
            big_center("Dash/SPA Welcomes"),
            big_center(name, id='name')
        ], className='jumbotron my-4')

    content = spa.Div(page_content(), id='content')

    @user.callback(content.output.children, [SpaComponents.url.input.pathname])
    def profile_cb(pathname):
        profile = page_content()
        return profile

    return html.Div(content)
