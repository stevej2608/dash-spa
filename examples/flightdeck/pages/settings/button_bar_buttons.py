from dash import html

from dash_spa.components.dropdown_button_aoi import DropdownButtonAIO, dropdownLink
from ..icons.hero import DOCUMENT, MESSAGE, UPLOAD, FIRE_DANGER, CALENDER

def newButton():
    return DropdownButtonAIO([
        dropdownLink("Document", DOCUMENT),
        dropdownLink("Message", MESSAGE),
        dropdownLink("Product", UPLOAD),
        dropdownLink("My Plan", FIRE_DANGER),
    ], "New")

def calenderButton():
    return  html.Button([
        CALENDER
    ], type='button', className='btn btn-gray-800 d-inline-flex align-items-center me-2')
