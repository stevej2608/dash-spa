import pytest
from dash_spa.components.table import TableState

def test_context():

    # _state = {'page_size' : 10, 'last_page' : None, 'current_page' : None, 'table_rows' : None}

    store = {}

    state = TableState()

    state.map_store(store)

    assert state.__store_keys__ == ['current_page', 'page_size', 'last_page', 'table_rows', 'search_term']

    with pytest.raises(AttributeError) as e_info:
        state.xxx = 99

    assert state.page_size == 10
    assert store['page_size'] == 10

    state.page_size = 25
    assert state.page_size == 25
    assert store['page_size'] == 25
