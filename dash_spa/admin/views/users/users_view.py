from dash import html

from dash_spa.admin.views.view_common import blueprint as admin, validate_user

from .users_table import user_table
from .users_form import user_form

@admin.route('/users', title='Admin Users', access=validate_user)
def user_view(ctx):

    table = user_table(ctx, ctx.login_manager)
    modal_form = user_form(ctx, table, ctx.login_manager)

    return html.Div([
        html.H2('Users'),
        table,
        modal_form,
    ])
