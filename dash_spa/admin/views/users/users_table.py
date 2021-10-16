import dash_datatables as ddt
from .user_data import user_db

def user_table(ctx, login_manager):

    df = user_db(login_manager.database_uri())

    columns = [{"title": i, "data": i} for i in df.columns]

    return ddt.DashDatatables(
        id = ctx.prefix('user-table'),
        columns=columns,
        data=df.to_dict('records'),
        column_defs = [{"targets": [ 0 ],"visible" : False }],
        editable=True
    )
