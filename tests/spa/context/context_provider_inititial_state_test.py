from typing import List
import pytest
import dash
from dash import html
from dash_spa.spa_context import  createContext, ContextState, dataclass

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
    toolbars: List[TBState] = None

def test_simple_state():
    app = dash.Dash(__name__)

    # Init btn1 with defaults

    btn1 = TButton()
    assert btn1.name == ""
    assert btn1.clicks == 0
    assert btn1.asdict() == {'name': '', 'clicks': 0}

    # Confirm dot notation works and dict is updated

    btn1.clicks = 1234
    assert btn1.clicks == 1234
    assert btn1.asdict()['clicks'] == 1234

    # Init btn2 with attribute values

    btn2 = TButton('test', 29)
    assert btn2.name == "test"
    assert btn2.clicks == 29
    assert btn2.asdict() == {'name': 'test', 'clicks': 29}

    # Confirm state is updated when new dict is assigned

    btn2.update(state={'name': 'test', 'clicks': 999})
    assert btn2.clicks == 999


def test_complex_state():
    app = dash.Dash(__name__)

    # Create a complex ContextState

    tb1 = TBState("main", ['close', "exit", 'refresh'])
    tb2 = TBState("page", ['next', "prev", 'top', 'bottom'])
    state = ToolbarList(toolbars=[tb1, tb2])

    # Confirm dot notation works

    assert state.toolbars[0].title  == 'main'
    assert state.toolbars[0].buttons[0].name  == 'close'

    # Confirm builtin asdict works

    state_asdict = state.asdict()
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

    # Change an element in the ContextState and confirm the dict
    # is updated in sympathy

    state.toolbars[0].buttons[0].clicks += 1

    assert state.asdict() == {'toolbars': [
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
    app = dash.Dash(__name__)

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

        initial_state=ToolbarList(toolbars=[tb1, tb2])
        state, _ = ToolbarContext.useState(initial_state=initial_state)

        return html.Div()

    layout()

    # A few sanity checks

    assert ToolbarContext.ctx == None
    assert 'test' in ToolbarContext.ctx_lookup

    # Confirm state has been initialised correctly

    state_asdict = state.asdict()
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
