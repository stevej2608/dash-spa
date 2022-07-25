from typing import List
import pytest
from dash import html
from dash_spa.logging import log
from dash_spa.spa_context import  createContext, ContextState, asdict, dataclass, EMPTY_LIST

# https://github.com/konradhalas/dacite

@dataclass
class TButton(ContextState):
    """State of a single button"""
    name: str = ''
    clicks: int = 0

@dataclass
class TBState(ContextState):
    """State of button toolbar"""

    title: str
    buttons: List[TButton]

    def __post_init__(self):
        self.buttons = [TButton(name, 0) for name in self.buttons]

@dataclass
class ToolbarList(ContextState):
    """State of several toolbars"""
    toolbars: List[TBState] = EMPTY_LIST

def test_simple_state():

    # Init btn1 with defaults

    btn1 = TButton()
    assert btn1.name == ""
    assert btn1.clicks == 0

    # Confirm shadow store is updated

    btn1_store = {}
    btn1.set_shadow_store(btn1_store)
    assert btn1_store == {'name': '', 'clicks': 0}

    # Confirm dot notation works and shadow store is updated

    btn1.clicks = 1234
    assert btn1.clicks == 1234
    assert btn1_store['clicks'] == 1234

    # Init btn2 with attribute values

    btn2 = TButton('test', 29)
    assert btn2.name == "test"
    assert btn2.clicks == 29

    # Confirm shadow store is updated

    btn2_store = {}
    btn2.set_shadow_store(btn2_store)
    assert btn2_store == {'name': 'test', 'clicks': 29}

    # Confirm state is updated when new shadow store is assigned

    btn2_new = {'name': 'test', 'clicks': 999}
    btn2.set_shadow_store(btn2_new)
    assert btn2.clicks == 999

    # Confirm the new shadow store tracks state changes

    btn2.clicks = 1000
    assert btn2.clicks == 1000
    assert btn2_new['clicks'] == 1000

    btn2.clicks += 1
    assert btn2.clicks == 1001
    assert btn2_new['clicks'] == 1001


def test_complex_state():

    # Create a complex ContextState

    tb1 = TBState("main", ['close', "exit", 'refresh'])
    tb2 = TBState("page", ['next', "prev", 'top', 'bottom'])
    state = ToolbarList(toolbars=[tb1, tb2])

    # Confirm dot notation works

    assert state.toolbars[0].title  == 'main'
    assert state.toolbars[0].buttons[0].name  == 'close'

    # Confirm builtin asdict works

    state_asdict = asdict(state)
    assert state_asdict == {'toolbars': [
                                {'title': 'main', 'buttons': [
                                    {'name': 'close', 'clicks': 0},
                                    {'name': 'exit', 'clicks': 0},
                                    {'name': 'refresh', 'clicks': 0}
                                    ]},
                                {'title': 'page', 'buttons': [
                                    {'name': 'next', 'clicks': 0},
                                    {'name': 'prev', 'clicks': 0},
                                    {'name': 'top', 'clicks': 0},
                                    {'name': 'bottom', 'clicks': 0}
                                    ]}
                                ]
                            }

    # Confirm shadow store gets updated as soon as it's assigned

    state_asdict = {}
    state.set_shadow_store(state_asdict)
    assert state_asdict == {'toolbars': [
                                {'title': 'main', 'buttons': [
                                    {'name': 'close', 'clicks': 0},
                                    {'name': 'exit', 'clicks': 0},
                                    {'name': 'refresh', 'clicks': 0}
                                    ]},
                                {'title': 'page', 'buttons': [
                                    {'name': 'next', 'clicks': 0},
                                    {'name': 'prev', 'clicks': 0},
                                    {'name': 'top', 'clicks': 0},
                                    {'name': 'bottom', 'clicks': 0}
                                    ]}
                                ]
                            }

    # Change an element in the ContextState and confirm the shadow store
    # is updated in sympathy

    state.toolbars[0].buttons[0].clicks += 1

    assert state_asdict == {'toolbars': [
                                {'title': 'main', 'buttons': [
                                    {'name': 'close', 'clicks': 1},
                                    {'name': 'exit', 'clicks': 0},
                                    {'name': 'refresh', 'clicks': 0}
                                    ]},
                                {'title': 'page', 'buttons': [
                                    {'name': 'next', 'clicks': 0},
                                    {'name': 'prev', 'clicks': 0},
                                    {'name': 'top', 'clicks': 0},
                                    {'name': 'bottom', 'clicks': 0}
                                    ]}
                                ]
                            }


def test_useState():

    ToolbarContext = createContext(ToolbarList)

    # Confirm context cannot be accessed outside of a Context.Provider

    with pytest.raises(Exception) as error:
        ToolbarContext.useState()
    assert "Context can only be used within the scope of a provider" in str(error)

    # State is only assigned here to allow later inspection

    state: ContextState = None

    # Confirm we can initialise and access ToolbarContext within a Provider scope

    @ToolbarContext.Provider(id='test')
    def layout():
        nonlocal state

        tb1 = TBState("main", ['close', "exit", 'refresh'])
        tb2 = TBState("page", ['next', "prev", 'top', 'bottom'])

        state, _ = ToolbarContext.useState(initial_state=ToolbarList([tb1, tb2]))

        return html.Div()

    layout()

    # A few sanity checks

    assert ToolbarContext.ctx == None
    assert 'test' in ToolbarContext.ctx_lookup

    # Confirm state has been initialised correctly

    state_asdict = asdict(state)
    assert state_asdict == {'toolbars': [
                                {'title': 'main', 'buttons': [
                                    {'name': 'close', 'clicks': 0},
                                    {'name': 'exit', 'clicks': 0},
                                    {'name': 'refresh', 'clicks': 0}
                                    ]},
                                {'title': 'page', 'buttons': [
                                    {'name': 'next', 'clicks': 0},
                                    {'name': 'prev', 'clicks': 0},
                                    {'name': 'top', 'clicks': 0},
                                    {'name': 'bottom', 'clicks': 0}
                                    ]}
                                ]
                            }


