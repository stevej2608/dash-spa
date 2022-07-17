from dash import html

from dash_spa.components.dropdown_button_aoi import DropdownButtonAIO, dropdownLink
from ..icons.hero import ICON

def reportsDropdown():
    return DropdownButtonAIO([
        dropdownLink("Products", ICON.PRODUCTS,href='#'),
        dropdownLink("Customers", ICON.CUSTOMERS, href='#'),
        dropdownLink("Orders", ICON.ORDERS, href='#'),
        dropdownLink("Console", ICON.CONSOLE, href='#'),
        html.Div(role='separator', className='dropdown-divider my-1'),
        dropdownLink("All Reports", ICON.ALL_REPORTS, href='#')
    ], "Reports", buttonIcon=ICON.CLIPBOARD, buttonColor="gray-800", downArrow=True)
