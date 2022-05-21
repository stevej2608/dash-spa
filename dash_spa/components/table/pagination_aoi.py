from typing import List
from math import ceil
from dash import html, callback, ALL
from dash.exceptions import PreventUpdate
from dash_prefix import match, prefix
from .PaginationState import PaginationState

from dash_spa.components import  AIOBase
from dash_spa.components.store_aio import StoreAIO

from dash_spa.logging import log


# Smart pagination algorithm, converted from PHP
# see: https://stackoverflow.com/a/163825/489239

class TableAIOPaginator(AIOBase):
    """Ellipses pagination component

    Args:
        page (int, optional): The initial active page. Defaults to 1.
        adjacents (int, optional): How many adjacent pages should be shown on each side. Defaults to 2.
        page_size (int, optional): How many items to show per page. Defaults to 5.
        total_items (int): Total number of items to be grouped into pages

    Example:

    ```

            « previous [1] 2 3 4 5 6 7 ... 19 20 NEXT »
            « PREVIOUS 1 [2] 3 4 5 6 7 ... 19 20 NEXT »
            « PREVIOUS 1 2 [3] 4 5 6 7 ... 19 20 NEXT »
            « PREVIOUS 1 2 3 [4] 5 6 7 ... 19 20 NEXT »
            « PREVIOUS 1 2 ... 3 4 [5] 6 7 ... 19 20 NEXT »

            « PREVIOUS 1 2 ... 13 14 [15] 16 17 ... 19 20 NEXT »
            « PREVIOUS 1 2 ... 14 15 [16] 17 18 19 20 NEXT »

            « PREVIOUS 1 2 ... 14 15 16 17 18 [19] 20 NEXT »
            « PREVIOUS 1 2 ... 14 15 16 17 18 19 [20] next »

    ```
    """

    PREVIOUS = 'Previous'
    NEXT = 'Next'

    @property
    def value(self):
        return self.store.input.data

    def __init__(self, page = 1, adjacents = 2, page_size = 5, total_items=None, className: str = None, id=None):
        self.pid = prefix(id)
        self.page=page
        self.adjacents=adjacents
        self.className = className
        self.range_match = match({'type': self.pid('li'), 'idx': ALL})
        self.lastpage = ceil(total_items / page_size)
        self.store = StoreAIO.create_store({'page': page, 'page_size': page_size, 'last_page': self.lastpage}, id=self.pid('store'))

        pagination = self.selectable(page, self.adjacents)
        self.container = html.Ul(pagination, id=self.pid('TableAIOPaginator'), className=self.className)

        @callback(self.store.output.data,
                  self.container.output.children,
                  self.range_match.input.n_clicks,
                  self.range_match.state.children,
                  self.store.state.data)
        def update_paginator_cb(clicks, children, data):
            log.info('update_paginator_cb')

            if not any(clicks):
                raise PreventUpdate

            # Set the selected element to active and update
            # store.data['page'] with the selected value

            page = data['page']

            index = self.range_match.triggerIndex()
            if index is not None:

                selection = self.selection(children[index])

                if selection == 'Previous':
                    page -=1
                elif selection == 'Next':
                    page += 1
                else:
                    page = selection

                data['page'] = page
                search = f"?page={page}"
                pagination = self.selectable(page, self.adjacents)

                return data, pagination

            raise PreventUpdate

    def layout(self, page=1): # pylint: disable=arguments-differ
        log.info('layout pge %s', page)
        self.container.children = self.selectable(page, self.adjacents)
        return self.container

    def state(self, state:dict = None) -> PaginationState:
        state = state if state else self.store.data
        return PaginationState(state)

    def selection(self, element: html.Li) -> str:
        """Return the selected page|Previous|Next

        Given the selected child element access and return the
        selected page from the HTML markup

        Args:
            children (html.Li): Selected child element

        Returns:
            str: page|Previous|Next
        """
        return element[0]['props']['children']


    def selectable(self, page:int, adjacents=2) -> List[html.Li]:
        """Return pagination child UI elements for given active page. Add
        Dash callback IDs to the child elements that we want to trigger a
        callback when clicked

        Args:
            page (int): The currently selected (active) page
            adjacents (int, optional): How many adjacent pages should be shown on each side. Defaults to 2.

        Returns:
            List[html.Li]: Pagination child elements
        """

        pagination = self.select(page, adjacents)

        # Create a list of elements that we want to trigger a callback when
        # clicked.

        selectable = [e for e in pagination if not ('active' in e.className or 'dissabled' in e.className)]

        for idx, element in enumerate(selectable):
            element.id = self.range_match.idx(idx)

        return pagination

    def select(self, page:int, adjacents=2) -> List[html.Li]:
        """Return pagination child UI elements for given active page

        Args:
            page (int): The currently selected (active) page
            adjacents (int, optional): How many adjacent pages should be shown on each side. Defaults to 2.

        Returns:
            List[html.Li]: Pagination child elements
        """

        pagination = []
        lastpage = self.lastpage

        def emit(page, active=False, disabled=False):
            element = self.emit(page, active, disabled)
            return [element]

        first_pages = emit(1) + emit(2)
        last_pages = emit(lastpage - 1) + emit(lastpage)

        # Previous button

        pagination += emit(self.PREVIOUS, disabled = page == 1)

        # Determin pages & ellipses to include...

        # Test to see if we have enough pages to bother breaking it up

        if lastpage < 7 + (adjacents * 2):
            for i in range(1, lastpage+1):
                pagination += emit(i, i == page)
        elif lastpage > 5 + (adjacents * 2):

            # Test to see if we're close to beginning. If so only hide later pages

            if page < 2 + (adjacents * 2):

                # eg, PREVIOUS 1 [2] 3 4 5 6 7 ... 19 20 NEXT

                for i in range(1, 5 + (adjacents * 2)):
                    pagination += emit(i, i == page)

                pagination += emit('...', disabled=True)
                pagination += last_pages

            elif page < lastpage - (1 + adjacents * 2):

                # We're in the middle hide some front and some back
                # eg, PREVIOUS 1 2 ... 5 6 [7] 8 9 ... 19 20 NEXT

                pagination += first_pages
                pagination += emit('...', disabled=True)

                for i in range(page - adjacents, page + adjacents + 1):
                    pagination += emit(i, i == page)

                pagination += emit('...', disabled=True)
                pagination += last_pages
            else:

                # Must be close to end only hide early pages
                # eg, PREVIOUS 1 2 ... 14 15 16 17 [18] 19 20 NEXT

                pagination += first_pages
                pagination += emit('...', disabled=True)

                for i in range(lastpage - (3 + (adjacents * 2)), lastpage + 1):
                    pagination += emit(i, i == page)

        # Append the Next button

        pagination += emit(self.NEXT, disabled=(page == lastpage))

        if lastpage <= 1 :
            pagination = []

        return pagination

    def emit(self, page: str, active=False, disabled=False) -> html.Li:
        """Return the html.Li markup for given page

        Args:
            page (str): The page number | Prev | Next | ellipses
            active (bool, optional): True if the page is the active page. Defaults to False.
            disabled (bool, optional): True of the page is not clickable. Defaults to False.

        Returns:
            html.Li: _description_
        """
        element = html.Li([html.Span(page, className='page-link')], className='page-item')
        if disabled:
            element.className += ' dissabled'
        if active:
            element.className += ' active'

        return element
