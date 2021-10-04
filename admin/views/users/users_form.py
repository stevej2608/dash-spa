import dash_bootstrap_components as dbc
import dash_holoniq_components as dhc
import dash_html_components as html

from .user_data import user_db

def user_form(spa, table, database_uri):

    user_form = dhc.Form([], id=spa.prefix('user-form'), preventDefault=True)
    cancel_btn = dbc.Button("Cancel", id=spa.prefix("close-btn"), className="ml-1", n_clicks=0)

    def form_body(action="blank_form", row_data=None):
        """Return form that's fully populated with relevant fields and buttons for the given action"""

        def form_builder(form, buttons):

            def form_field(label, name, value):
                return dbc.FormGroup([dbc.Label(label), dbc.Input(name=name, value=value)])

            form.children = [

                # Hidden fields used to report the table row id & action

                dbc.Input(name='id', type="hidden", value=row_data['id']),
                dbc.Input(name='action', type="hidden", value=action),

                form_field("Name", "name", row_data['name']),
                form_field("email", "email", row_data['email']),
                form_field("role", "role", row_data['role']),

                dbc.ButtonGroup(buttons, className='float-right mt-2')
            ]
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
            form = [user_form, cancel_btn]

        return [
            dbc.ModalHeader(header),
            dbc.ModalBody(form),
        ]

    modal_form = dbc.Modal(form_body(), id=spa.prefix("modal"), is_open=False)


    @spa.callback(
        [modal_form.output.is_open, modal_form.output.children],
        [table.input.table_event, cancel_btn.input.n_clicks, user_form.input.form_data])
    def toggle_modal(table_evt, close_btn, value):
        is_open = False
        form = spa.NOUPDATE

        df = user_db(database_uri)

        def new_id():
            id = df['id'].max()
            return id + 1 if id == id else 0

        # Populate modal form fields based on table event

        if spa.isTriggered(table.input.table_event):
            action = table_evt['action']
            if action == "add_row":
                id = new_id()
                row_data = {'id': id, 'name': '', 'email': '', 'role': ''}

            else:
                row_data = table_evt['data']
            form = form_body(action, row_data)
            is_open = True

        elif close_btn or value:
            is_open = False

        return is_open, form

    @spa.callback(table.output.data, user_form.input.form_data)
    def table_update(value):
        table_data = spa.NOUPDATE

        df = user_db(database_uri)

        if value:
            action = value['action']
            user_data = {
                "id": int(value['id']),
                "email": value["email"],
                "name": value["name"],
                "role": value["role"],
            }

            if action == 'add_row':
                df = df.append(user_data, ignore_index=True)

            if action == 'delete_row':
                id = user_data['id']
                df = df[df.id != id]

            if action == 'edit_row':
                id = user_data['id']
                keys, values = zip(*user_data.items())
                df.loc[df['id'] == id, keys] = values

        table_data = df.to_dict('records')
        return table_data

    return html.Div(modal_form)
