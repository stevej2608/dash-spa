from dataclasses import dataclass
from dash_spa.spa_context import createContext, ContextState

@dataclass
class TableState(ContextState):
    current_page: int = 1
    page_size: int = 10
    last_page: int = 1
    table_rows: int = 0
    search_term: str = ''

TableContext = createContext(TableState);