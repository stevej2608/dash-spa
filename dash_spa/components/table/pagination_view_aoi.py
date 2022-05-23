from dash import html, callback
from dash.exceptions import PreventUpdate
from dash_spa import  prefix
from dash_redux import ReduxStore, StateWrapper
from dash_spa.logging import log

class TableAIOPaginatorView(html.Div):
    """Manages and updates the view component of the associated
    TableAIOPaginator. The TableAIOPaginatorView callback is triggered when the
    store component value changes. The callback calls the supplied
    'content' function. The function return value is rendered as the child
    element of the TableAIOPaginatorView

    Args:
        paginator (TableAIOPaginator): The associated paginator
        className (str): the className of the component

    Returns:
        html.Div: The view component

    Example:
    ```

        paginator = TableAIOPaginator(["Previous", 1, 2, 3, 4, 5, "Next"], 5, 25)
        viewer = TableAIOPaginatorView(paginator, render_content, className='fw-normal small mt-4 mt-lg-0' )
    ```

    Markup:
    ```
        <div class="fw-normal small mt-4 mt-lg-0">
            Showing page <b>4</b> out of <b>25</b> pages
        </div>
    ```
    """
    def __init__(self, store: ReduxStore, className='fw-normal small mt-4 mt-lg-0', id=None):
        pid = prefix(id)
        state = StateWrapper(store.data)
        content = self.render_content(state.current_page, state.last_page)

        super().__init__(content, id=pid('TableAIOPaginator'), className=className)

        @callback(self.output.children, store.store.input.data)
        def update_paginator_view_cb(store):
            if store is not None:
                store = StateWrapper(store)
                # log.info('update_paginator_view_cb(id=%s) page=%d', pid(''), store.current_page)
                return self.render_content(store.current_page, store.last_page)

            raise PreventUpdate

    def render_content(self, current, last_page):
        return ["Showing page ",html.B(current)," out of ",html.B(last_page)," pages"]
