from dash_spa.spa_context import createContext, ContextState, dataclass

@dataclass
class TableState(ContextState):
    current_page: int = 1
    page_size: int = 10
    last_page: int = 1
    table_rows: int = 0
    search_term: str = None

TableContext = createContext(TableState)