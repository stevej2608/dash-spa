from dash import html, callback
from dash.exceptions import PreventUpdate
from dash_spa.components import  AIOBase
from .pagination_aoi import TableAIOPaginator

from dash_spa.logging import log

class TableAIOPaginatorView(AIOBase):

    def __init__(self, paginator: TableAIOPaginator, className='fw-normal small mt-4 mt-lg-0'):
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
        id=paginator.pid('TableAIOPaginatorView')
        state = paginator.state()

        self.container = html.Div(self.render_content(state.page, state.last_page), id=id, className=className)

        @callback(self.container.output.children, paginator.value)
        def update_paginator_view_cb(data):
            log.info('update_paginator_view_cb')

            if data is not None:
                state = paginator.state(data)
                return self.render_content(state.page, state.last_page)

            raise PreventUpdate

    def layout(self):
        return self.container

    def render_content(self, current, last_page):
        return ["Showing page ",html.B(current)," out of ",html.B(last_page)," pages"]
