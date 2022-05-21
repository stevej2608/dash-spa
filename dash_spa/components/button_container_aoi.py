from dash_spa.logging import log
from typing import Callable, List
from dash import html, dcc, callback, ALL
from dash.exceptions import PreventUpdate
from dash_spa import match, prefix, isTriggered

from dash_spa.components.store_aio import StoreAIO

class Dict2Obj:
    def __init__(self, d=dict) -> object:
        if d is not None:
            for key, value in d.items():
                setattr(self, key, value)

class ButtonContainerAIO(html.Div):

    def __init__(self, range: List, current:str, range_element: Callable, className: str = None, aio_id=None):

        self.store = store = StoreAIO.create_store({'range': range, 'current': current}, aio_id)

        pid = prefix(self.store.id)

        data = Dict2Obj(store.data)

        range_match = match({'type': pid('li'), 'idx': ALL})

        def _range_element(index, text):
            rng = range_element(text, text==current)
            return html.Div(rng, id=range_match.idx(text))

        range_elements = [_range_element(index, text) for index, text in enumerate(data.range)]

        @callback(store.output.data,
                  range_match.output.children,
                  range_match.input.n_clicks,
                  store.state.data)
        def update_container(clicks, data):

            #log.info('click')

            if not any(clicks):
                raise PreventUpdate

            # Call the supplied range_element() for each container
            # element and set store.data['current'] with the currently
            # selected value

            children_out = []
            for index, element in enumerate(range_elements):
                text = range_elements[index].id['idx']
                if isTriggered(element.input.n_clicks):
                    log.info('click %s', text)
                    data['current'] = text
                    children = range_element(text, True)
                else:
                    children = range_element(text, False)

                children_out.append(children)

            return data, children_out

        super().__init__(range_elements.copy(), id=pid('ButtonContainerAIO'), className=className)
