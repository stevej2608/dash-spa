from abc import abstractmethod
from typing import List, Dict, Any
from dash import html, callback

from dash_spa import AIOBase, prefix

from holoniq.utils import log

from .pagination_aoi import TableAIOPaginator

TableData = List[Dict[str, Any]]
TableColumns = List[Dict[str, Any]]

class TableAIO(AIOBase):

    TABLE_CLASS_NAME = ''

    def __init__(self, data: TableData, columns: TableColumns, page_size: int = None, id: str = None):
        self.pid = prefix(id)
        self.data = data
        self.page_size = page_size

        # pylint: disable=assignment-from-none
        self.paginator = self.paginator_init(page=1, page_size=page_size, total_items=len(data))

        self.table = self.table_init(data, columns, page_size=page_size)

    def layout(self, page=1):  # pylint: disable=arguments-differ
        log.info('layout page %s', page)
        self.table.children[1] = self.tableBody(self.data, page=page, page_size=self.page_size)
        container = html.Div([self.table], className=self.TABLE_CLASS_NAME)
        if self.paginator:
            container.children += [self.paginator.layout(page)]

        return container

    def table_init(self, data, columns: TableColumns, page=1, page_size = None):
        thead = self.tableHead(columns)
        tbody = self.tableBody(data, page=1, page_size=page_size)
        table = html.Table([thead,tbody], className='table table-hover', id=self.pid('table'))

        if self.paginator:

            @callback(table.output.children, self.paginator.value)
            def _update_table_cb(paginator_state):
                log.info('_update_table_cb')
                state = self.paginator.state(paginator_state)
                tbody = self.tableBody(data, page=state.page, page_size=state.page_size)
                return [thead, tbody]

        return table

    def paginator_init(self, page:int, page_size, total_items) -> TableAIOPaginator:
        """Return paginator to be used with the table"""
        return None

    def tableHead(self, columns: TableColumns):
        row =  html.Tr([html.Th(col['name'], className='border-gray-200') for col in columns])
        return html.Thead(row)

    def tableBody(self, data, page=1, page_size = None):
        if page_size:
            low = (page -1) * page_size
            high = (page) * page_size
            high = high if high < len(data) else len(data)
            data = data[low:high]
        return html.Tbody([self.tableRow(args) for args in data])

    @abstractmethod
    def tableRow(self, args):
        return None

