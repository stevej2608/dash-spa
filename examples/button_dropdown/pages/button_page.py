from typing import List

from dash import html
from dash_spa import register_page, prefix, trigger_index

from dash_spa.spa_context import createContext, ContextState, dataclass
from dash_spa.components import DropdownAIO, ButtonContainerAIO, SPA_NOTIFY, Notyf

from .icons import ICON

page = register_page(__name__, path='/', title="Button Test", short_name='Buttons')

# See assets.css for icon and test styling

@dataclass
class TableState(ContextState):
    page_size: int = 10

TableContext: TableState = createContext(TableState)

class PageSizeSelect(ButtonContainerAIO):

    className ='dropdown-menu dropdown-menu-xs dropdown-menu-end pb-0'

    def __init__(self, page_sizes: List, current:int, id):
        super().__init__(page_sizes, current, id=id, className=PageSizeSelect.className)

        state = TableContext.getState()

        @TableContext.On(self.button_match.input.n_clicks)
        def page_select(clicks):
            index = trigger_index()
            if index is not None and clicks[index]:
                state.page_size = int(page_sizes[index])


    def render_buttons(self, elements):
        state = TableContext.getState()

        def render_button(text):
            if int(text) == state.page_size:
                element = html.Div([text, ICON.TICK], className='dropdown-item d-flex align-items-center fw-bold')
            else:
                element = html.Div(text, className='dropdown-item fw-bold')

            if text == elements[-1]:
                element.className += ' rounded-bottom'
            return element

        return [render_button(text) for text in elements]

def page_size_dropdown(id) -> html.Div:
    pid = prefix(id)

    button = DropdownAIO.Button([
       ICON.GEAR,html.Span("Toggle Dropdown", className='visually-hidden')
    ], className='btn btn-link text-dark dropdown-toggle dropdown-toggle-split m-0 p-1')

    container = PageSizeSelect(["10", "20", "30"], 0, id=pid('settings_container'))
    dropdown = DropdownAIO(button, container, id=pid('settings_dropdown'))

    return html.Div(dropdown)

@TableContext.Provider()
def layout():
    state = TableContext.getState()
    size_dropdown = page_size_dropdown('test')
    h4 = html.H4(f"Page size is {state.page_size}")

    @SPA_NOTIFY.update(TableContext.store.input.data)
    def btn_cb(data, store):
        notyf = Notyf(message=f'Page size is {state.page_size}', type='info')
        return notyf.report()

    return html.Div([h4, size_dropdown])
