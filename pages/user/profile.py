from dash import html
from flask_login import current_user

from dash_spa import register_page, current_user, login_required
from pages import USER_SLUG

register_page(__name__, path=USER_SLUG, title="Dash - Profile", short_name='User')

# NOTE: This page is used by pytest. The id='user-name' is
# used as part of the admin_login_test to confirm the test user
# has logged in successfully. The id would normally not be needed.

# This page is hidden from guest visitors by @login_required

@login_required
def layout():

    def big_center(text, id=None):
        if id:
            return html.H2(text, id=id, className='display-3 text-center')
        else:
            return html.H2(text, className='display-3 text-center')

    def page_content():
        name = current_user.name

        return html.Header([
            big_center("Dash/SPA Welcomes"),
            big_center(name, id='user-name')
        ], className='jumbotron my-4')

    content = html.Div(page_content(), id='content')
    return html.Div(content)
