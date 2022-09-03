from typing import List

from dash import html
from dash_spa import register_page
from dash_spa.components.dropdown_button_aoi import DropdownButtonAIO, dropdownLink


from .icons import ICON

page = register_page(__name__, path='/dropdown', title="Dropdown Test", short_name='Dropdown')

class MyDropdown(DropdownButtonAIO):

    container_className = 'dropdown-menu dashboard-dropdown dropdown-menu-start mt-2 py-1'

    def button_className(self, buttonColor):
        return f'btn btn-{buttonColor} d-inline-flex align-items-center me-2 dropdown-toggle'


def newButton():
    return MyDropdown([
        dropdownLink("Document", ICON.DOCUMENT),
        dropdownLink("Message", ICON.MESSAGE.ME2),
        dropdownLink("Product", ICON.UPLOAD),
        dropdownLink("My Plan", ICON.FIRE.ME2_DANGER),
    ], "New")


def buttonBar(lhs=[], rhs=[]):
    lhs = lhs if isinstance(lhs, list) else [lhs]
    rhs = rhs if isinstance(rhs, list) else [rhs]
    return html.Div([
        *lhs,
        html.Div(rhs, className='d-flex flex-md-nowrap align-items-center')
    ], className='d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center py-4')


layout = html.Div([
        buttonBar(
            lhs=newButton(),
        ),
    ], style={"min-height": "100%"})
