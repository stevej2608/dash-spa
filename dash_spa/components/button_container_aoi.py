from typing import Callable, List
from dash_redux import ReduxStore
from dash_spa.logging import log
from dash import html, dcc, callback, ALL
from dash_spa import match, prefix, isTriggered, trigger_index, NOUPDATE


class Dict2Obj:
    def __init__(self, d=dict) -> object:
        if d is not None:
            for key, value in d.items():
                setattr(self, key, value)

class ButtonContainerAIO(html.Div):

    def __init__(self, range: List, current:int, store: ReduxStore, className: str = None, id=None):

        id = prefix(store.store.id) if id is None else id
        pid = prefix(id)

        self._elements = range

        range_match = match({'type': pid('li'), 'idx': ALL})

        def _range_elements(current):

            def _range_element(index, text):
                rng = self.render_element(text, index==current)
                return html.Div(rng, id=range_match.idx(index))

            return [_range_element(index, text) for index, text in enumerate(range)]

        range_elements = _range_elements(current)

        @callback(range_match.output.children, range_match.input.n_clicks)
        def _update_cb(clicks):

            def _range_elements(current):
                return [self.render_element(text, index==current) for index, text in enumerate(range)]

            index = trigger_index()
            log.info('update UI index= %s', index)

            if index is not None and clicks[index]:
                range_elements = _range_elements(index)
                return range_elements.copy()

            return NOUPDATE

        @store.update(range_match.input.n_clicks)
        def _update_store(clicks, store):
            index = trigger_index()
            if index is not None and clicks[index]:
                store = self.update_function(index, store)
                log.info('store = %s', store)
                return store

            return NOUPDATE

        super().__init__(range_elements, id=pid('ButtonContainerAIO'), className=className)

    def render_element(self, selected_index):
        pass

    def update_function(self, value, store):
        pass

