from dash import html

from admin.views.view_common import blueprint as admin, validate_user

from .users_table import user_table
from .users_form import user_form

@admin.route('/users', title='Admin Users', access=validate_user)
def user_view(ctx):
    spa = admin.get_spa()

    database_uri = ctx.login_manager.database_uri()

    table = user_table(spa, ctx.login_manager)
    modal_form = user_form(spa, table, ctx.login_manager)

    return html.Div([
        html.H2('Users'),
        table,
        modal_form,
    ])
