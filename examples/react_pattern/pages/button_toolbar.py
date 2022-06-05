from dash import html, ALL
from dash_spa import prefix, NOUPDATE, add_style
from dash_spa.logging import log
from dash_spa.spa_context import createContext
import dash_spa as spa

ButtonContext = createContext();

def button_toolbar(title, buttons, id):
    pid = prefix(id)
    state, set_state = ButtonContext.useState(title, [{'id': btn, 'clicks' : 0} for btn in buttons])

    button_match = spa.match({'type': pid('btn'), 'idx': ALL})

    btns = html.Div([
        html.Button(title, id=button_match.idx(index), type="button", className='btn btn-secondary me-1')
        for index, title in enumerate(buttons)
        ]
    )

    msg = [f"{btn.id} pressed {btn.clicks} times" for btn in state]
    container = html.H5(", ".join(msg))

    @ButtonContext.On(button_match.input.n_clicks, prevent_initial_call=True)
    def btn_update(clicks):
        index = spa.trigger_index()
        state[index].clicks += 1
        set_state(state)

    return html.Div([btns, container], style={'background-color': '#e6e6e6'})
