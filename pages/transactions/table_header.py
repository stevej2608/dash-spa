from dash import html, dcc, ALL
from dash_svg import Svg, Path
from dash_spa import match, prefix
from dash_spa.components.dropdown_aio import DropdownAIO
from dash_spa.components.button_container_aoi import ButtonContainerAIO
from .icons import TICK_ICON, GEAR_ICON

from dash_spa.components.table import TableAIO, PAGE_SIZE, LAST_PAGE, CURRENT_PAGE


def _searchOrders():
    return  html.Div([
        html.Div([
            html.Span([
                Svg([
                    Path(fillRule='evenodd', d='M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z', clipRule='evenodd')
                ], className='icon icon-xs', xmlns='http://www.w3.org/2000/svg', viewBox='0 0 20 20', fill='currentColor', **{"aria-hidden": "true"})
            ], className='input-group-text'),
            dcc.Input(type='text', className='form-control', placeholder='Search orders')
        ], className='input-group me-2 me-lg-3 fmxw-400')
    ], className='col col-md-6 col-lg-3 col-xl-4')


def _settingsDropdown(table: TableAIO) -> html.Div:

    button = DropdownAIO.Button([
       GEAR_ICON,html.Span("Toggle Dropdown", className='visually-hidden')
    ], className='btn btn-link text-dark dropdown-toggle dropdown-toggle-split m-0 p-1')


    def element_renderer(value, selected):
        if selected:
            element = html.Div([value, TICK_ICON], className='dropdown-item d-flex align-items-center fw-bold')
        else:
            element = html.Div(value, className='dropdown-item fw-bold')

        if value == "30":
            element.className += ' rounded-bottom'

        return element

    page_sizes = ["10", "20", "30"]

    pid = table.prefix('settings')

    def update_function(value, store):
        store[PAGE_SIZE] = new_size = int(page_sizes[value])
        store[LAST_PAGE] = table.last_row(new_size)
        store[CURRENT_PAGE] = 1
        return store

    container = ButtonContainerAIO(page_sizes, 0,
                    element_renderer, table.store, update_function,
                    className='dropdown-menu dropdown-menu-xs dropdown-menu-end pb-0',
                    id=pid('container'))

    # container.children[0:0] = [html.Span("Show", className='small ps-3 fw-bold text-dark')]

    dropdown = DropdownAIO(button, container)

    return html.Div(dropdown, className='col-4 col-md-2 col-xl-1 ps-md-0 text-end')


def create_header(table: TableAIO) -> html.Div:
    return html.Div([
        html.Div([
            _searchOrders(),
            _settingsDropdown(table),
        ], className='row align-items-center justify-content-between')
    ], className='table-settings mb-4')
