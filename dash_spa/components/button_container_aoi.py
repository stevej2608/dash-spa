from abc import abstractmethod
from typing import List
from dash_redux import ReduxStore
from dash_spa.logging import log
from dash import html, callback, ALL
from dash.development.base_component import Component
from dash_spa import match, prefix, trigger_index, NOUPDATE


class Dict2Obj:
    def __init__(self, d=dict) -> object:
        if d is not None:
            for key, value in d.items():
                setattr(self, key, value)

class ButtonContainerAIO(html.Div):
    """Manage a container(typically a list) of buttons and associated
    store. This is an abstract base class.

    Args:
        elements (List[str]): The button text
        current (int): Index of the selected button
        store (ReduxStore): Store to be updated when a button is clicked
        className (str, optional): Container className. Defaults to None.
        id (_type_, optional): Container ID, if None one will be allocated.

    Abstract Methods:

        render_button(self, text, selected)

        update_store(self, value, store)

    """

    def __init__(self, elements: List, current:int, store: ReduxStore, className: str = None, id=None):
        id = prefix(store.id) if id is None else id
        pid = prefix(id)
        self._elements = elements
        button_match = match({'type': pid('li'), 'idx': ALL})

        def _render_buttons(current):

            buttons = self.render_buttons(store.data)

            def _render_button(index, text):
                btn = buttons[index]
                return html.Div(btn, id=button_match.idx(index))

            return [_render_button(index, text) for index, text in enumerate(elements)]

        buttons = _render_buttons(current)

        @store.update(button_match.input.n_clicks)
        def _update_store(clicks, store):

            # Button clicked update the store

            index = trigger_index()

            if index is not None and clicks[index]:
                store = self.update_store(index, store)
                log.info('store = %s', store)
                return store

            return NOUPDATE


        @callback(button_match.output.children, store.input.data)
        def _update_cb(store):

            # Store has changed, update buttons

            buttons = self.render_buttons(store)
            return buttons


        super().__init__(buttons, id=pid('ButtonContainerAIO'), className=className)

    @abstractmethod
    def render_buttons(self, store:ReduxStore) -> List[Component]:
        """Return a button component list"""
        pass

    @abstractmethod
    def update_store(self, value, store: ReduxStore) -> ReduxStore :
        pass

