from typing import Callable
from abc import abstractmethod
from math import ceil
from typing import List, Dict, Any
from dash import html, callback
# from dash_redux import ReduxStore, StateWrapper

import dash_spa as spa
from dash_spa.logging import log

from .context import TableContext, PAGE_SIZE, LAST_PAGE, CURRENT_PAGE, TABLE_ROWS

TableData = List[Dict[str, Any]]
TableColumns = List[Dict[str, Any]]

class TableAIO(html.Table):
    """Generic SPA Table

    Args:
        data (TableData): The table data (an array of dict)
        columns (TableColumns): Column names dictionary
        page (int, optional): Initial page size. Defaults to 1.
        page_size (int, optional): Initial page size. Defaults to 100.
        id (str, optional): The table id. If None one will be assigned.

    Notes:

        The table needs to be initialised with a *page_size* that is the
        largest that will ever be displayed

    """

    TABLE_CLASS_NAME = 'table table-hover'

    def __init__(self, data: TableData, columns: TableColumns, page = 1, page_size: int = 100, id: str = None, **kwargs):

        initial_state = {
            CURRENT_PAGE : page,
            LAST_PAGE : ceil(len(data) / page_size),
            PAGE_SIZE: page_size,
            TABLE_ROWS: len(data)
        }

        state, _ = TableContext.useState(initial_state=initial_state)

        self._prefix = pid = spa.prefix(id)
        self._data = data

        log.info('TableAIO id=%s', pid())

        thead = self.tableHead(columns)
        trows = self.tableRows(data, page=state.current_page, page_size=page_size)
        tbody = html.Tbody(trows, id=pid('table'))

        super().__init__([thead,tbody], className=TableAIO.TABLE_CLASS_NAME, **kwargs)

    def tableHead(self, columns: TableColumns):
        row =  html.Tr([html.Th(col['name'], className='border-gray-200') for col in columns])
        return html.Thead(row)

    def tableRows(self, data, page=1, page_size = None):
        if page_size:
            low = (page -1) * page_size
            high = (page) * page_size
            high = high if high < len(data) else len(data)
            data = data[low:high]
        return[self.tableRow(index, args) for index, args in enumerate(data)]

    @abstractmethod
    def tableRow(self, row_index, args):
        return None

