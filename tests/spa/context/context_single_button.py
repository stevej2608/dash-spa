import dash
import re
import plotly
import json
from dash import html
from dash_spa.spa_context import createContext, ContextState, dataclass

@dataclass
class ButtonState(ContextState):
    clicks: int = 1000

ButtonContext = createContext(ButtonState)

def componentDecode(comp):

    # ReduxStore elements use a hash() to generate a component
    # id. This is a problem when testing because the hash() seed changes
    # on each test run. Here we pick out the hash based ids' and replace
    # them with an index.

    id_list = []

    def replace_id(match):
        val = match.group(0).split(': ')[1]
        if val not in id_list:
            id_list.append(val)
        return f"\"idx\": \"PYTEST_REPLACEMENT_ID_{id_list.index(val)}\""

    # "idx": "2438d368d91cd816"

    json_str = json.dumps(comp, cls=plotly.utils.PlotlyJSONEncoder)
    json_str = re.sub(r'\"idx\": \"[0-9a-f]+\"', replace_id, json_str)

    return json.loads(json_str)

def test_single_button(dash_duo):
    app = dash.Dash(__name__)

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

    # Test code

    def wait_text(text):
        return dash_duo.wait_for_text_to_equal(div.css_id, text, timeout=4)

    browser_btn = dash_duo.find_element(btn.css_id)

    assert wait_text("Button pressed 1000 times!")

    browser_btn.click()
    assert wait_text("Button pressed 1001 times!")

    expected = {
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
                "children": "Button pressed 1000 times!",
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
                        "clicks": 1001
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
                        "clicks": 1001
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


    res = componentDecode(app.layout)
    assert res == expected
