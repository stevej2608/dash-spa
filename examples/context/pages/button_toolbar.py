from typing import List, Dict
from dash import html, ALL
from dash_spa import prefix
from dash_spa.logging import log
from dash_spa.spa_context import  createContext, ContextState, dataclass
import dash_spa as spa


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

ToolbarContext: Dict[str, TBState] = createContext()

def button_toolbar(id, initial_state:TBState):
    pid = prefix(f'button_toolbar_{id}')

    state, _ = ToolbarContext.useState(id, initial_state=initial_state)

    log.info("button_toolbar state.id=%s (%s)", pid(), state.cid())

    button_match = spa.match({'type': pid('btn'), 'idx': ALL})

    btns = html.Div([
        html.Button(btn.name, id=button_match.idx(idx), type="button", className='btn btn-secondary me-1')
        for idx, btn in enumerate(state.buttons)
        ]
    )

    msg = [f"{btn.name} pressed {btn.clicks} times" for btn in state.buttons]
    container = html.H5(", ".join(msg))

    @ToolbarContext.On(button_match.input.n_clicks)
    def btn_update(clicks):
        log.info("btn_update state.cid=%s", state.cid())
        index = spa.trigger_index()
        state.buttons[index].clicks += 1

    title = html.H4(f"Toolbar {state.title}")

    return html.Div([title, btns, container], style={'background-color': '#e6e6e6'})
