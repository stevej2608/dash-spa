from typing import List
from dash import html
from dash_spa import prefix, trigger_index
from dash_spa.components.dropdown_aio import DropdownAIO
from dash_spa.components.button_container_aoi import ButtonContainerAIO
from ..icons.hero import TICK_ICON, GEAR_ICON

from dash_spa.components.table import SearchAIO, TableContext


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
                state.last_page = int(state.table_rows / state.page_size)
                state.current_page = 1

    def render_buttons(self, elements):
        state = TableContext.getState()

        def render_button(text):
            if int(text) == state.page_size:
                element = html.Div([text, TICK_ICON], className='dropdown-item d-flex align-items-center fw-bold')
            else:
                element = html.Div(text, className='dropdown-item fw-bold')

            if text == elements[-1]:
                element.className += ' rounded-bottom'
            return element

        return [render_button(text) for text in elements]


def _settingsDropdown(id) -> html.Div:
    pid = prefix(id)

    button = DropdownAIO.Button([
       GEAR_ICON,html.Span("Toggle Dropdown", className='visually-hidden')
    ], className='btn btn-link text-dark dropdown-toggle dropdown-toggle-split m-0 p-1')

    container = PageSizeSelect(["10", "20", "30"], 0, id=pid('settings_container'))
    dropdown = DropdownAIO(button, container, id=pid('settings_dropdown'))

    return html.Div(dropdown, className='col-4 col-md-2 col-xl-1 ps-md-0 text-end')


def create_header(id) -> html.Div:
    """Create the search input and page size drop-down"""

    search = SearchAIO(id=id, placeholder='Search customers')

    return html.Div([
        html.Div([
            search,
            _settingsDropdown(id=id),
        ], className='row align-items-center justify-content-between')
    ], className='table-settings mb-4')
