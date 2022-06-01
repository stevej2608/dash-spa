from flask import current_app as app
from dash_spa.logging import log
from dash_redux import ReduxStore
from munch import DefaultMunch


# https://www.digitalocean.com/community/tutorials/how-to-share-state-across-react-components-with-context

class _ContextWrapper:

    @property
    def input(self):
        return self.store.input

    @property
    def output(self):
        return self.store.output

    @property
    def state(self):
        return self.store.state

    def __init__(self, **kwargs):
        self.id = kwargs.pop('_id')
        self.props = kwargs.copy()


    def On(self, *_args, **_kwargs):
        """Transform a @ctx.On(...) callback an @store.update()
        callback on the internal contexts store
        """

        def wrapper(user_func):

            def callback_stub(self, *_args, **_kwargs):
                pass

            if app and app.got_first_request:
                return callback_stub

            log.info("register callback %s", self.id)

            @self.store.update(*_args)
            def _proxy(*_args):
                prev_props = self.props.copy()

                # pop the store reference

                args = list(_args)
                store = args.pop()

                user_func(*args)

                if prev_props != self.props:
                    new_state = self.props.copy()
                    self.props = DefaultMunch.fromDict(new_state)
                    store = new_state

                return store

        return wrapper

    def Provider(self, props=None):

        # props can be provide when the context is created or passed in here

        self.props = DefaultMunch.fromDict(props.copy() if props is not None else self.props)
        self.store = ReduxStore(id=self.id, data=self.props)

        def provider_decorator(func):

            def func_wrapper( *_args, **_kwargs):

                # Call the Dash layout function we've wrapped

                result = func(*_args, **_kwargs)

                # Inject the context store into the layout

                if not isinstance(result.children, list):
                    result.children = [result.children]

                result.children.append(self.store)

                return result

            self.render = func_wrapper

            return func_wrapper
        return provider_decorator


def createContext(props={}, id=None):
    return _ContextWrapper(**props, _id=id)

def useContext(ctx: _ContextWrapper):
    return ctx
