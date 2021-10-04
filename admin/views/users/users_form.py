import dash_bootstrap_components as dbc
import dash_holoniq_components as dhc
import dash_html_components as html

from .user_data import user_db

def user_form(spa, table, login_manager):

    user_form = dhc.Form([], id=spa.prefix('user-form'), preventDefault=True)
    cancel_btn = dbc.Button("Cancel", id=spa.prefix("close-btn"), className="ml-1", n_clicks=0)

    def form_body(action="blank_form", row_data=None):
        """Return form that's fully populated with relevant fields and buttons for the given action"""

        def form_builder(form, buttons):

            def form_field(label, name, value):
                disabled = action == 'delete_row'
                return dbc.FormGroup([dbc.Label(label), dbc.Input(name=name, value=value, disabled=disabled)])

            form.children = [

                # Hidden fields used to report the user id and table action

                dbc.Input(name='action', type="hidden", value=action),

                form_field("Name", "name", row_data['name']),
                form_field("email", "email", row_data['email']),
                form_field("password", "password", ''),
                form_field("role", "role", row_data['role']),

                dbc.ButtonGroup(buttons, className='float-right mt-2')
            ]

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
            header = "New user"
            form = form_builder(user_form, [add_btn, cancel_btn])

        elif action == 'delete_row':
            header = "Delete user"
            form = form_builder(user_form, [delete_btn, cancel_btn])

        elif action == 'edit_row':
            header = "Edit user"
            form = form_builder(user_form, [edit_btn, cancel_btn])

        else:
            form = user_form
            form.children = cancel_btn

        return [
            dbc.ModalHeader(header),
            dbc.ModalBody(form),
        ]

    modal_form = dbc.Modal(form_body(), id=spa.prefix("modal"), is_open=False)

    # Process table action, set up and show the modal form

    @spa.callback(
        [modal_form.output.is_open, modal_form.output.children],
        [table.input.table_event, cancel_btn.input.n_clicks, user_form.input.form_data])
    def toggle_modal(table_evt, close_btn, value):
        is_open = False
        form = spa.NOUPDATE

        # Populate modal form fields based on table event

        if spa.isTriggered(table.input.table_event):
 
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

    @spa.callback(table.output.data, user_form.input.form_data)
    def table_update(value):
        table_data = spa.NOUPDATE


        if value:
            action = value['action']

            del value['submit_count']
            del value['action']

            if action == 'add_row':
                login_manager.add_user(**value)

            if action == 'delete_row':
                login_manager.delete_user(value['email'])

            if action == 'edit_row':
                login_manager.update_user(**value)


        df = user_db(login_manager.database_uri())

        table_data = df.to_dict('records')
        return table_data

    return html.Div(modal_form)
