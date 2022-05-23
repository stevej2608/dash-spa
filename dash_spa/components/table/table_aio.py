from abc import abstractmethod
from math import ceil
from typing import List, Dict, Any
from dash import html, callback
from dash_redux import ReduxStore, StateWrapper

from dash_spa import prefix, PreventUpdate, page_container_append
from dash_spa.logging import log


TableData = List[Dict[str, Any]]
TableColumns = List[Dict[str, Any]]

class TableAIO(html.Div):
    """Generic SPA Table

    Args:
        data (TableData): The table data (an array of dict)
        columns (TableColumns): Column names dictionary
        page (int, optional): Initial page size. Defaults to 1.
        page_size (int, optional): Initial page size. Defaults to 10.
        id (str, optional): The table id. If None one will be assigned.
        """

    TABLE_CLASS_NAME = ''

    def __init__(self, data: TableData, columns: TableColumns, page = 1, page_size: int = 10, id: str = None):

        self.pid = prefix(id)

        log.info('TableAIO id=%s', self.pid(''))

        table_data = {
            'data': data,
            'current_page': page,
            'last_page' : ceil(len(data) / page_size),
            'page_size': page_size
        }

        self.store = store = ReduxStore(id=self.pid('store'), data=table_data)
        page_container_append(store)

        thead = self.tableHead(columns)
        trows = self.tableRows(data, page=1, page_size=page_size)
        tbody = html.Tbody(trows, id=self.pid('table'))

        @callback(tbody.output.children, store.store.input.data)
        def _update_table_cb(store):
            try:
                store = StateWrapper(store)
                log.info('_update_table_cb')
                rows = self.tableRows(store.data, page=store.current_page, page_size=store.page_size)
                return rows
            except:
                raise PreventUpdate()

        table = html.Table([thead,tbody], className='table table-hover')
        super().__init__(table, className=self.TABLE_CLASS_NAME)


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

