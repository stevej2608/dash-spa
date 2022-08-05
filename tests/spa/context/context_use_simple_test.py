from typing import Dict, List
import pytest
from dash import html
from dash_spa.spa_context import createContext, ContextState, dataclass, field

@dataclass
class ButtonState(ContextState):
    clicks: int = 10

ButtonContext = createContext(ButtonState)

def test_context_simple():

    # Try and use context outside of provider - exception expected

    with pytest.raises(Exception):
        state = ButtonContext.getState()

    # Use two context providers with same
    # ButtonContext. Confirm they don't interfere with each other

    @ButtonContext.Provider()
    def layout_test1(expected):
        state = ButtonContext.getState()
        assert state.clicks == expected
        state.clicks = expected + 10
        return html.Div()

    @ButtonContext.Provider()
    def layout_test2(expected):
        state = ButtonContext.getState()
        assert state.clicks == expected
        state.clicks = expected + 10
        return html.Div()

    for value in [10, 20, 30, 40]:
        layout_test1(value)
        layout_test2(value)

    # Confirm ButtonState dataclass is unchanged

    assert ButtonState.clicks == 10
