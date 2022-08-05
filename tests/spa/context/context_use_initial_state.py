from typing import Dict, List
import pytest
from dash import html
from dash_spa.spa_context import createContext, ContextState, dataclass, field

@dataclass
class TButton(ContextState):
    name: str = ''
    clicks: int = 0

@dataclass
class TBState(ContextState):
    title: str = ""
    buttons: List[TButton] = None

    def __post_init__(self):
        self.buttons = [TButton(name, 0) for name in self.buttons]

ToolbarContext = createContext()

def test_context_initial_state():

    state = None

    @ToolbarContext.Provider(id='tb_test')
    def toolbar_layout(id, initial_state:TBState):
        nonlocal state
        state, _ = ToolbarContext.useState(id, initial_state=initial_state)
        return html.Div()

    toolbar_layout('main', TBState("main", ['close', "exit", 'refresh']))

    state = ToolbarContext.get_context_state('tb_test')
    assert state.main.buttons[0].name == 'close'
