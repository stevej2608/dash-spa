import pytest
from dash_spa.spa_context import ContextState
from dataclasses import dataclass

@dataclass
class TableState(ContextState):
    current_page: int = 1
    page_size: int = 10
    last_page: int = 1
    table_rows: int = 0
    search_term: str = None


def test_context():

    # Create a TableState

    state = TableState()
    assert state.__store_keys__ == ['current_page', 'page_size', 'last_page', 'table_rows', 'search_term']

    # Back the TableState with a store and confirm store values shadow the TableState

    store = {}
    state.map_store(store)

    assert store == {'current_page': 1, 'page_size': 10, 'last_page': 1, 'table_rows': 0, 'search_term': None}

    # Confirm we can only write specific values

    with pytest.raises(AttributeError) as e_info:
        state.xxx = 99

    assert state.page_size == 10

    # Change a TableState attribute and confirm the value is updated

    state.page_size = 25
    assert state.page_size == 25
    assert store == {'current_page': 1, 'page_size': 25, 'last_page': 1, 'table_rows': 0, 'search_term': None}

    # Update TableState

    state.update(state=TableState(2, 30, 100, 1000))
    assert state.current_page == 2
    assert store == {'current_page': 2, 'page_size': 30, 'last_page': 100, 'table_rows': 1000, 'search_term': None}

    # Map new store

    store = {'current_page': 99, 'page_size': 130, 'last_page': 130, 'table_rows': 2000, 'search_term': 'AAA'}
    state.map_store(store)

    assert state.current_page == 99
    assert state.search_term == 'AAA'



