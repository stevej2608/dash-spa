from typing import List
from dash import html, dcc, ALL
from dash_svg import Svg, Path
from dash_spa import match, prefix, trigger_index
from dash_spa.components.dropdown_aio import DropdownAIO
from dash_spa.components.button_container_aoi import ButtonContainerAIO
from .icons import TICK_ICON, GEAR_ICON, SEARCH_ICON

from dash_spa.components.table.context import TableContext, PAGE_SIZE


def _searchOrders(id):
    pid = prefix(id)

    search_term, setSearchTerm = TableContext.useState('search_term', '')

    search = dcc.Input(id=pid('search'), className='form-control', type="text", value=search_term, placeholder='Search orders')

    @TableContext.On(search.input.value, prevent_initial_call=True)
    def search_cb(value):
        setSearchTerm(value)

    return  html.Div([
        html.Div([
            html.Span(SEARCH_ICON, className='input-group-text'),
            search
        ], className='input-group me-2 me-lg-3 fmxw-400')
    ], className='col col-md-6 col-lg-3 col-xl-4')



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
    return html.Div([
        html.Div([
            _searchOrders(id=id),
            _settingsDropdown(id=id),
        ], className='row align-items-center justify-content-between')
    ], className='table-settings mb-4')
