import sys
from copy import deepcopy
from dash import dcc,  no_update as NOUPDATE
from dash import html, callback, ALL
from dash_spa import match,  prefix, trigger_index

# from dash_spa.logging import log

def default_action_execute(cmd, state, *_args, **_kwargs):
    """Built in action execute dispatcher"""
    state = StateWrapper(state)
    new_state = cmd(state, *_args, **_kwargs)
    return new_state.state

class ReduxStore(html.Div):
    """Create a master dcc.Store who's input is derived from any number surrogate stores that are
    presented to application for update. The (modified) content of a surrogate stores are copied to
    the master store. This mechanism acts as a data multiplexor feeding Dash UI events into a
    master "source of truth" that can then be used to trigger additional activity in the UI.

    The application interfaces with the store using the callback @Redux.update(...). This
    callback defines Dash IO to be used by the callback handler in the normal way. When
    triggered by a Dash event the associated function is called with the IO state together
    with a reference to a surrogate store that contains a copy of the master store. The callback
    modifies the state are required and returns the store state which is then copied into the
    master store.

    Usage:
    ```
        Redux = ReduxStore(id='store', data = { "todo": []})

        @Redux.update(button.input.n_clicks, input.state.value)
        def new_activity(button_clicks, input, state):
            if button_clicks and input:
                 state['todo'].append(input)
            return state
    ```

    Action dispatch callback returns an action_function reference. The
    action_function updates the store state:

    ```
    @Redux.action(button.input.n_clicks, input.state.value)
    def _add(button_clicks, input):
        if button_clicks and input:
            return add_action, input
        else:
            NOUPDATE

    # Example action_function

    def add_action(state, input):
        current = state.todo.copy()
        state.past.append(current)
        state.todo.append(input)
        state.future = []
        return state

    ```
    """

    @property
    def data(self):
        return self.master_store.data

    @property
    def store(self):
        return self.master_store

    def __init__(self, id, **kwargs):
        self.pfx = prefix(id)

        self.storage_type = kwargs.pop('storage_type', 'session')
        self.execute = kwargs.pop('execute', default_action_execute)

        self.master_store = dcc.Store(id=id, storage_type=self.storage_type, **kwargs)

        self._surrogate_store_match = match({'type': self.pfx('store'), 'idx': ALL})
        self._surrogate_stores = {}

        super().__init__([self.master_store])

        # MASTER store surrogate merge @callback

        @callback(self.master_store.output.data, self._surrogate_store_match.input.data, prevent_initial_call=True)
        def update_store(surrogate_state):

            # log.info('Updating MASTER state = %s', store_state)
            # for index, state in enumerate(mux_state):
            #     log.info('mux_state %02d  %s', index, state)

            index = trigger_index()
            if index is not None:
                # log.info('Update using index  = %d', index)
                return deepcopy(surrogate_state[index])

            return NOUPDATE


    def update(self, *_args, **_kwargs):
        """
        Used as a decorator, `@Redux.update` provides a server-side
        callback relating the values of one or more `Output` items to one or
        more `Input` items which will trigger the callback when they change,
        and optionally `State` items which provide additional information but
        do not trigger the callback directly.

        When triggered by a Dash event the associated function is called with
        the IO state together with a reference to a surrogate store that contains a
        copy of the master store. The callback modifies the state as required and
        returns the store state.  *ReduxStore* then copies the new state into
        the master store.

        Usage:
        ```
        Redux = ReduxStore(id='store', data=TODO_MODEL)

        @Redux.update(btn1.input.n_clicks)
        def btn1_update(clicks, store):
            if clicks:
                store['btn1'] += 1
                return store
            return NOUPDATE

        ```
        """
        surrogate_store = self._surrogate_input_store(*_args)

        def wrapper(user_func):

            @callback(surrogate_store.output.data, *_args, self.master_store.state.data, prevent_initial_call=True, **_kwargs)
            def _proxy(*_args):

                # We need to copy the state of the master store to make sure
                # it's immutable

                args = list(_args)
                args[-1] = deepcopy(args[-1])

                # Call the user's @Redux.update() function.

                result = user_func(*args)

                # Return the results to the standard Dash callback.
                # If the surrogate_store has been modified this will
                # trigger the `MASTER store surrogate merge @callback`

                return result

        return wrapper

    def action(self, *_args, **_kwargs):
        """
        Used as a decorator, `@Redux.action` provides a server-side
        callback relating the values of one or more `Output` items to one or
        more `Input` items which will trigger the callback when they change,
        and optionally `State` items which provide additional information but
        do not trigger the callback directly.

        When triggered by a Dash event the associated function is called with
        the IO state. Based on the IO state the function is expected to return
        a reference to an `action_function` together with any parameters that
        the action_function is expecting. ReduxStore calls the execute function
        that was provided when the store was initialised. The arguments passed
        to the execute function are the action_function, the store state and
        any callback parameters. The action_function updates the state as
        required. *ReduxStore* then copies the new state into the master
        store.

        Usage:
        ```
        Redux = ReduxStore(id='store', data=TODO_MODEL)

        @Redux.action(button.input.n_clicks, input.state.value)
        def _add(button_clicks, input):
            if button_clicks and input:
                return add_action, input
            else:
                NOUPDATE
        ```
        """
        surrogate_store = self._surrogate_input_store(*_args)

        def wrapper(user_func):

            @callback(surrogate_store.output.data, *_args, prevent_initial_call=True, **_kwargs)
            def _proxy(*_args):

                # Call the user's @Redux.action() function.

                result = user_func(*_args)

                # Test for a returned action_function

                if result != NOUPDATE and result != None:

                    # With arguments?

                    if callable(result):
                        action = result
                        args = []
                    else:
                        args = list(result)
                        action = args.pop(0)

                    # Execute the users action function

                    result = self.execute(action, surrogate_store.data, *args)

                    # Return the results to the standard Dash callback.
                    # If the surrogate_store has been modified this will
                    # trigger the `MASTER store surrogate merge @callback`

                else:
                    result = NOUPDATE

                return result

        return wrapper

    def _surrogate_input_store(self, *_args):

        # Surrogate stores are created and stored for reuse in
        # a dictionary that is keyed on a hash of all the input
        # IDs defined in the callback.

        def unpack(id):

            # Handle dict the keys used by MATCH

            if isinstance(id, dict):
                id = [ part for part in id.values() if isinstance(part, str)]
                return '_'.join(id)
            else:
                return id

        def input_hash():

            # Create a positive hex hash all the callback inputs

            inputs = []
            for input in _args:
                id = f"{unpack(input.component_id)}.{input.component_property}"
                # log.info('input %s', id)
                inputs.append(id)
            _hash = hash(tuple(inputs))
            _hash += sys.maxsize + 1
            return hex(_hash)[2:]

        id = input_hash()

        if not id in self._surrogate_stores:
            # log.info('Create Redux mux %s', id)
            match_id = self._surrogate_store_match.idx(id)
            store = dcc.Store(id=match_id, data=self.data, storage_type='memory')
            self._surrogate_stores[id] = store
            self.children.append(store)

        # log.info("number of mux inputs = %d", len(self._mux_stores))

        return self._surrogate_stores[id]


class StateWrapper:
    """Convenience class used to provide obj.attribute access to the
    model. Writes to attributes only update the wrapped copy NOT
    the master model.
    """

    def __init__(self, state):
        self.state = state

    def get(self, attr, default):
        if attr in self.state:
            return self.state[attr]
        else:
            self.state[attr] = default
            return default

    def __getattr__(self, key):
        if key in self.state:
            return self.state[key]
        raise AttributeError(f"error: attribute {key} has not been defined.")

    def __setattr__(self, key, value):
        if key is 'state':
            super(StateWrapper, self).__setattr__(key, value)
        elif key in self.state:
            self.state[key] = value
        else :
            raise AttributeError(f"error: attribute {key} has not been defined.")

