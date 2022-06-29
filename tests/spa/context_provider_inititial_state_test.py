from typing import List
from dash import html
from dash_spa.logging import log
from dash_spa.spa_context import  createContext, ContextState, asdict, dataclass, EMPTY_LIST

# https://github.com/konradhalas/dacite

@dataclass
class TButton(ContextState):
    name: str = ''
    clicks: int = 0

@dataclass
class TBState(ContextState):
    title: str
    buttons: List[TButton]

    def __post_init__(self):
        self.buttons = [TButton(name, 0) for name in self.buttons]

@dataclass
class ToolbarList(ContextState):
    toolbars: List[TBState] = EMPTY_LIST

TestContext = createContext(ToolbarList)


def test_dict_equal():

    dict1 = {
        'Country_name': 'U.S.A',
        'values': [56,78,97]
    }

    dict2 = {
        'Country_name': 'U.S.A',
        'values': [56,78,97]
    }

    dict3 = {
        'Country_name': 'U.S.A',
        'values': [56,99,97]
    }

    assert dict1 == dict2
    assert dict1 != dict3


def test_complex_state():
    tb1 = TBState("main", ['close', "exit", 'refresh'])
    tb2 = TBState("page", ['next', "prev", 'top', 'bottom'])
    state = ToolbarList(toolbars=[tb1, tb2])

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

    # Confirm incoming dict get updated

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


def test_useState_initial_state():

    state = None

    @TestContext.Provider(id='test')
    def layout():
        nonlocal state

        tb1 = TBState("main", ['close', "exit", 'refresh'])
        tb2 = TBState("page", ['next', "prev", 'top', 'bottom'])

        state, _ = TestContext.useState(initial_state=ToolbarList([tb1, tb2]))

        return html.Div()

    layout()

    state_asdict = asdict(state)

    assert state_asdict

