import pytest
from dash_spa.context_state import ContextState
from dataclasses import dataclass

@dataclass
class TableState(ContextState):
    current_page: int = 1
    page_size: int = 10
    last_page: int = 1
    table_rows: int = 0
    search_term: str = None


def test_context_wrapper():

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


def test_context_nesting():

    @dataclass
    class NodeState(ContextState):
        value: int = 10
        left = None
        right = None

    # Create a simple tree

    root = NodeState(1)
    left = NodeState(2)
    right = NodeState(3)

    root.left = left
    root.right = right

    # Confirm the tree values are accessible

    assert root.value == 1
    assert root.left.value == 2
    assert root.right.value == 3

    # Confirm a newly mapped store is updated correctly

    store = {}
    root.map_store(store)
    assert store == {'value': 1, 'left': {'value': 2}, 'right': {'value': 3}}

    # Confirm attribute changes are mapped to the store

    root.left.value = 88
    root.right.value = 99
    assert store == {'value': 1, 'left': {'value': 88}, 'right': {'value': 99}}

    # Confirm mapping a new store updates the attributes correctly

    store = {'value': 22, 'left': {'value': 33}, 'right': {'value': 44}}
    root.map_store(store)

    assert root.value == 22
    assert root.left.value == 33
    assert root.right.value == 44

    # Confirm nested update works

    new_tree = NodeState(100)
    new_tree.left = NodeState(200)
    root.update(state=new_tree)

    assert root.value == 100
    assert root.left.value == 200
    assert root.right.value == 44






