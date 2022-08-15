from flask import current_app as app
import pandas as pd

from dash import html
import dash_bootstrap_components as dbc
import dash_holoniq_components as dhc
import dash_datatables as ddt

from dash_spa import prefix, isTriggered, callback, NOUPDATE
from dash_spa.logging import log

from ..decorators import role_required


def user_db(database_uri) :
    df = pd.read_sql_table('user', database_uri)
    df = df.drop(['password'], axis=1)
    df.index = df['id']
    return df

def usersForm(table, database_uri):
    """Modal form that's used to edit the Users table"""

    user_form = dhc.Form([], id='user-form', preventDefault=True)
    cancel_btn = dbc.Button("Cancel", id="cancel-btn", type="reset", className="ml-1", n_clicks=0)

    def form_body(action="blank_form", row_data=None):
        """Return form that's fully populated with relevant fields and buttons for the given action"""

        def form_builder(form, buttons):

            def form_field(label, name, value):
                disabled = action == 'delete_row'
                return html.Div([
                    dbc.Label(label), dbc.Input(name=name, value=value, disabled=disabled)
                    ], className='mb-3')

            form.children = [

                # Hidden fields used to report the user id and table action

                dbc.Input(name='action', type="hidden", value=action),

                form_field("Name", "name", row_data['name']),
                form_field("Email", "email", row_data['email']),
                form_field("Role", "role", row_data['role']),

                html.Div(buttons, className='d-grid gap-2 d-md-flex justify-content-md-end')
            ]

            if action != 'delete_row':
                form.children.insert(3, form_field("Password", "password", ''))

            if 'id' in row_data:
                user_id = dbc.Input(name='id', type="hidden", value=row_data['id'])
                form.children.insert(0, user_id)

            return form

        header = "Header"

        # Only one of the folowing buttons appears on the form

        add_btn = dbc.Button('Add', type='submit', color="primary")
        delete_btn = dbc.Button('Delete', type='submit', color="primary")
        edit_btn = dbc.Button('Update', type='submit', color="primary")

        if action == 'add_row':
            header = "New User"
            form = form_builder(user_form, [add_btn, cancel_btn])

        elif action == 'delete_row':
            header = "Delete User"
            form = form_builder(user_form, [delete_btn, cancel_btn])

        elif action == 'edit_row':
            header = "Edit User"
            form = form_builder(user_form, [edit_btn, cancel_btn])

        else:
            form = user_form
            form.children = cancel_btn

        return [
            dbc.ModalHeader(header),
            dbc.ModalBody(form),
        ]

    modal_form = dbc.Modal(form_body(), id="modal", is_open=False)

    # Process table action, set up and show the modal form

    @callback(
        modal_form.output.is_open, modal_form.output.children,
        table.input.table_event, cancel_btn.input.n_clicks, user_form.input.form_data)
    def toggle_modal(table_evt, close_btn, value):
        is_open = False
        form = NOUPDATE

        # Populate modal form fields based on table event

        if isTriggered(table.input.table_event):

            action = table_evt['action']
            if action == "add_row":
                row_data = {'name': '', 'email': '', 'role': ''}

            else:
                row_data = table_evt['data']
            form = form_body(action, row_data)
            is_open = True

        elif close_btn or value:
            is_open = False

        return is_open, form

    # Process modal form close, use the form values to update the table

    @callback(table.output.data, user_form.input.form_data)
    def table_update(value):
        table_data = NOUPDATE


        if isTriggered(user_form.input.form_data) and value:
            action = value['action']

            del value['submit_count']
            del value['action']

            if action == 'add_row':
                app.login_manager.add_user(**value)

            if action == 'delete_row':
                app.login_manager.delete_user(value['email'])

            if action == 'edit_row':
                app.add_template_testlogin_manager.update_user(**value)


        df = user_db(database_uri)

        table_data = df.to_dict('records')
        return table_data

    return html.Div(modal_form)


def user_table(prefix, database_uri):

    df = user_db(database_uri)

    columns = [{"title": i, "data": i} for i in df.columns]

    return ddt.DashDatatables(
        id = prefix('user-table'),
        columns=columns,
        data=df.to_dict('records'),
        column_defs = [{"targets": [ 0 ],"visible" : False }],
        editable=True
    )

def usersView(ctx, database_uri):

    pfx = prefix('admin#users')
    table = user_table(pfx, database_uri)
    modal_form = usersForm(table, database_uri)

    @role_required('admin')
    def layout():
        return html.Div([html.H2('Users'), table, modal_form])

    return layout
