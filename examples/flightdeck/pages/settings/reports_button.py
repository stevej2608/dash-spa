from dash import html

from dash_spa.components.dropdown_button_aoi import DropdownButtonAIO, dropdownLink
from ..icons.hero import CLIPBOARD, PRODUCTS, CUSTOMERS, ORDERS, CONSOLE, ALL_REPORTS

def reportsDropdown():
    return DropdownButtonAIO([
        dropdownLink("Products", PRODUCTS,href='#'),
        dropdownLink("Customers", CUSTOMERS, href='#'),
        dropdownLink("Orders", ORDERS, href='#'),
        dropdownLink("Console", CONSOLE, href='#'),
        html.Div(role='separator', className='dropdown-divider my-1'),
        dropdownLink("All Reports", ALL_REPORTS, href='#')
    ], "Reports", buttonIcon=CLIPBOARD, buttonColor="gray-800", downArrow=True)
