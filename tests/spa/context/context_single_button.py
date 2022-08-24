from dash import html
from dash_spa.spa_context import createContext, ContextState, dataclass
from dash_spa.utils.dumps_layout import dumps_layout

@dataclass
class ButtonState(ContextState):
    clicks: int = 1000

ButtonContext = createContext(ButtonState)

def expected_layout(count):
    return {
        "props": {
            "children": [
            {
                "props": {
                "children": "Button",
                "id": "btn"
                },
                "type": "Button",
                "namespace": "dash_html_components"
            },
            {
                "props": {
                "children": f"Button pressed {count} times!",
                "id": "div"
                },
                "type": "Div",
                "namespace": "dash_html_components"
            },
            {
                "props": {
                "children": [
                    {
                    "props": {
                        "id": "test_provider",
                        "data": {
                        "clicks": count
                        },
                        "storage_type": "memory"
                    },
                    "type": "Store",
                    "namespace": "dash_core_components"
                    },
                    {
                    "props": {
                        "id": {
                        "type": "test_provider_ip",
                        "idx": "PYTEST_REPLACEMENT_ID_0"
                        },
                        "data": {
                        "clicks": count
                        },
                        "storage_type": "memory"
                    },
                    "type": "Store",
                    "namespace": "dash_core_components"
                    }
                ],
                "id": "test_provider#container"
                },
                "type": "Div",
                "namespace": "dash_html_components"
            }
            ],
            "id": "test_provider_ctx_container"
        },
        "type": "Div",
        "namespace": "dash_html_components"
        }


def test_single_button(dash_duo, app):

    # Create Dash UI and start the test server

    btn, div = None, None

    @ButtonContext.Provider(id='test_provider')
    def layout():
        nonlocal btn, div

        state = ButtonContext.getState()
        btn = html.Button("Button", id='btn')

        @ButtonContext.On(btn.input.n_clicks, prevent_initial_call=True)
        def btn_click(clicks):
            state.clicks += 1

        div = html.Div(f"Button pressed {state.clicks} times!", id='div')

        return html.Div([btn, div])

    app.layout = layout()
    dash_duo.start_server(app)

    # Confirm the initial component tree layout

    res = dumps_layout(app.layout)
    assert res == expected_layout(count=1000)

    # Confirm the initial browser UI

    def browser_wait_text(text):
        return dash_duo.wait_for_text_to_equal(div.css_id, text, timeout=4)

    assert browser_wait_text("Button pressed 1000 times!")

    # Click a button and confirm the browser UI is updated

    browser_btn = dash_duo.find_element(btn.css_id)
    browser_btn.click()
    assert browser_wait_text("Button pressed 1001 times!")

    # Confirm the new component tree layout

    _layout = layout()
    res = dumps_layout(_layout)
    assert res == expected_layout(count=1001)