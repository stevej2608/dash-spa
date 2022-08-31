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
    """Manage a container of buttons. This is an abstract base class.

    The ButtonContainerAIO constructor calls the render_button() method
    passing in the list of elements. It then wraps each button in the
    returned button list in a callback match ALL container. The button_match
    attribute can then be used in by the super-class to action button callback
    events.

    Args:
        elements (List): List of elements to be passed to the render() method.
        current (int): Index of the selected button
        className (str, optional): Container className. Defaults to None.
        id (_type_, optional): Container ID.

    Attributes:

        button_match: Match ALL button id to be used in callbacks

    Abstract Methods:

        render_buttons(self, elements)

    """

    def __init__(self, elements: List, current:int, className: str = None, id=None):

        assert id, "The ButtonContainerAIO must have an id"

        pid = prefix(id)
        self._elements = elements

        self.button_match = match({'type': pid('li'), 'idx': ALL})

        def _render_buttons(current):

            # Get the user rendered button list

            buttons = self.render_buttons(elements)

            def _render_button(index, text):
                btn = buttons[index]
                return html.Div(btn, id=self.button_match.idx(index))

            return [_render_button(index, text) for index, text in enumerate(elements)]

        buttons = _render_buttons(current)

        super().__init__(buttons, className=className)

    @abstractmethod
    def render_buttons(self, elements:List) -> List[Component]:
        """Return a list of button components derived from the supplied
        element list.

        Args:
            elements (List): elements to be rendered

        Returns:
            List[Component]: Elements rendered as buttons
        """

        return []

