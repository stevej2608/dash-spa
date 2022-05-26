from typing import Callable
from abc import abstractmethod
from math import ceil
from typing import List, Dict, Any
from dash import html, callback
from dash_redux import ReduxStore, StateWrapper

import dash_spa as spa
from dash_spa.logging import log

TableData = List[Dict[str, Any]]
TableColumns = List[Dict[str, Any]]

PAGE_SIZE = 'page_size'
LAST_PAGE = 'last_page'
CURRENT_PAGE = 'current_page'

class TableAIO(html.Table):
    """Generic SPA Table

    Args:
        data (TableData): The table data (an array of dict)
        columns (TableColumns): Column names dictionary
        page (int, optional): Initial page size. Defaults to 1.
        page_size (int, optional): Initial page size. Defaults to 10.
        id (str, optional): The table id. If None one will be assigned.
        """

    TABLE_CLASS_NAME = 'table table-hover'

    @property
    def config(self):
        if self.config_store.store.data:
            return self.config_store.data
        else:
            return self._initial_config

    def __init__(self, data: TableData, columns: TableColumns, page = 1, page_size: int = 10, id: str = None, **kwargs):

        self._prefix = pid = spa.prefix(id)
        self._data = data

        log.info('TableAIO id=%s', pid(''))

        self._initial_config = {
            CURRENT_PAGE : page,
            LAST_PAGE : ceil(len(data) / page_size),
            PAGE_SIZE: page_size
        }


        self.config_store = store = ReduxStore(id=pid('store'), data={}, storage_type="local")
        spa.page_container_append(store)

        thead = self.tableHead(columns)
        trows = self.tableRows(data, page=1, page_size=page_size)
        tbody = html.Tbody(trows, id=pid('table'))

        @callback(tbody.output.children, store.input.data)
        def _update_table_cb(store):
            try:
                if store:
                    log.info('_update_table_cb(id=%s) live store=%s', pid(''), store)
                else:
                    log.info('_update_table_cb(id=%s) init store=%s', pid(''), store)
                    store = self._initial_config

                store = StateWrapper(store)
                rows = self.tableRows(data, page=store.current_page, page_size=store.page_size)
                return rows
            except:
                raise spa.PreventUpdate()

        super().__init__([thead,tbody], className=TableAIO.TABLE_CLASS_NAME, **kwargs)


    def prefix(self, pfx:str = None) -> Callable[[str], str]:
        return spa.prefix(f'{self._prefix(pfx)}')

    def last_row(self, page_size):
        return ceil(len(self._data) / page_size)

    def tableHead(self, columns: TableColumns):
        row =  html.Tr([html.Th(col['name'], className='border-gray-200') for col in columns])
        return html.Thead(row)

    def tableRows(self, data, page=1, page_size = None):
        if page_size:
            low = (page -1) * page_size
            high = (page) * page_size
            high = high if high < len(data) else len(data)
            data = data[low:high]
        return[self.tableRow(args) for args in data]

    @abstractmethod
    def tableRow(self, args):
        return None

