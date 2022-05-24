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

    def __init__(self, range: List, current:int,
                       range_element: Callable,
                       store: ReduxStore, update_function,
                       className: str = None, aio_id=None):

        pid = prefix(store.store.id)

        range_match = match({'type': pid('li'), 'idx': ALL})

        def _range_elements(current):

            def _range_element(index, text):
                rng = range_element(text, index==current)
                return html.Div(rng, id=range_match.idx(text))

            return [_range_element(index, text) for index, text in enumerate(range)]

        range_elements = _range_elements(current)

        @callback(range_match.output.children, range_match.input.n_clicks)
        def _update_cb(clicks):

            def _range_elements(current):
                return [range_element(text, index==current) for index, text in enumerate(range)]

            index = trigger_index()
            if index is not None and clicks[index]:
                log.info('update UI  index= %s', index)
                range_elements = _range_elements(index)
                return range_elements

            return NOUPDATE

        # @store.update(range_match.input.n_clicks)
        # def _update_store(clicks, store):
        #     index = trigger_index()
        #     if index is not None and clicks[index]:
        #         store = update_function(index, store)
        #         log.info('store = %s', store)
        #         return store

        #     return NOUPDATE


        super().__init__(range_elements, id=pid('ButtonContainerAIO'), className=className)
