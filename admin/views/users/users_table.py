import dash_datatables as ddt
from .user_data import user_db

def user_table(spa, database_uri):

    df = user_db(database_uri)

    columns = [{"title": i, "data": i} for i in df.columns]

    return ddt.DashDatatables(
        id = spa.prefix('user-table'),
        columns=columns,
        data=df.to_dict('records'),
        width="100%",
        order=[2, 'asc'],
        editable=True
    )
 
