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
        id = prefix(store.store.id) if id is None else id
        pid = prefix(id)
        self._elements = elements
        button_match = match({'type': pid('li'), 'idx': ALL})

        def _render_buttons(current):
            def _render_button(index, text):
                btn = self.render_button(text, index==current)
                return html.Div(btn, id=button_match.idx(index))
            return [_render_button(index, text) for index, text in enumerate(elements)]

        buttons = _render_buttons(current)

        @callback(button_match.output.children, button_match.input.n_clicks)
        def _update_cb(clicks):

            def _render_buttons(current):
                return [self.render_button(text, index==current) for index, text in enumerate(elements)]

            index = trigger_index()
            log.info('update UI index= %s', index)

            if index is not None and clicks[index]:
                buttons = _render_buttons(index)
                return buttons.copy()

            return NOUPDATE

        @store.update(button_match.input.n_clicks)
        def _update_store(clicks, store):
            index = trigger_index()
            if index is not None and clicks[index]:
                store = self.update_store(index, store)
                log.info('store = %s', store)
                return store

            return NOUPDATE

        super().__init__(buttons, id=pid('ButtonContainerAIO'), className=className)

    @abstractmethod
    def render_button(self, text) -> Component:
        """Return a button component for he given value

        Args:
            text (str): Text for button
        """
        pass

    @abstractmethod
    def update_store(self, value, store: ReduxStore) -> ReduxStore :
        pass

