import pytest
from dash import html
from dash_spa.spa_context import createContext, ContextState, dataclass, field


def test_context_simple():

    @dataclass
    class ButtonState(ContextState):
        clicks: int = 10

    ButtonContext = createContext(ButtonState);

    # Try and use context outside of provider - exception expected

    with pytest.raises(Exception):
        state = ButtonContext.getState()

    # Use two context providers with same
    # ButtonContext. Confirm they don't interfere with each other

    @ButtonContext.Provider(id='test1')
    def layout_test1(expected):
        state = ButtonContext.getState()
        assert state.clicks == expected
        state.clicks = expected + 10
        return html.Div()

    @ButtonContext.Provider(id='test2')
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


def test_context_list():

    @dataclass
    class SizesState(ContextState):
        size: int = 10
        sizes: list = field(default_factory=lambda: [10, 20, 30])

    SizesContext = createContext(SizesState);

    @SizesContext.Provider(id='test1')
    def layout_test1(expected):
        state = SizesContext.getState()
        assert state.sizes[0] == expected
        state.sizes[0] = expected + 10
        return html.Div()

    for value in [10, 20, 30, 40]:
        layout_test1(value)

   # Confirm ButtonState dataclass is unchanged

    assert SizesState.size == 10


def test_context_dict():

    @dataclass
    class ColourState(ContextState):
        selected: str = 'red'
        colours: list = field(default_factory=lambda: ['red', 'green', 'blue'])

    ColourContext = createContext(ColourState);

    @ColourContext.Provider(id='test1')
    def layout_test1(index):
        state = ColourContext.getState()
        assert state.selected == state.colours[index]
        state.selected = state.colours[index+1]
        return html.Div()

    for value in [0, 1]:
        layout_test1(value)
