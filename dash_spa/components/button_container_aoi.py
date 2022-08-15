from abc import abstractmethod
from typing import List
from dash_redux import ReduxStore
from dash_spa.logging import log
from dash import html, ALL
from dash.development.base_component import Component
from dash_spa import callback, match, prefix, trigger_index, NOUPDATE


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

    def __init__(self, elements: List, current:int, className: str = None, id=None):

        assert id, "The ButtonContainerAIO must have an id"

        pid = prefix(id)
        self._elements = elements
        self.button_match = match({'type': pid('li'), 'idx': ALL})

        def _render_buttons(current):

            buttons = self.render_buttons(elements)

            def _render_button(index, text):
                btn = buttons[index]
                return html.Div(btn, id=self.button_match.idx(index))

            return [_render_button(index, text) for index, text in enumerate(elements)]

        buttons = _render_buttons(current)

        super().__init__(buttons, className=className)

    @abstractmethod
    def render_buttons(self, store:ReduxStore) -> List[Component]:
        """Return a button component list"""
        pass

