from dash import html

from dash_spa.components.dropdown_button_aoi import DropdownButtonAIO, dropdownLink
from ..icons.hero import ICON

def newButton():
    return DropdownButtonAIO([
        dropdownLink("Document", ICON.DOCUMENT),
        dropdownLink("Message", ICON.MESSAGE),
        dropdownLink("Product", ICON.UPLOAD),
        dropdownLink("My Plan", ICON.FIRE.ME2_DANGER),
    ], "New")

def calenderButton():
    return  html.Button([
        ICON.CALENDER
    ], type='button', className='btn btn-gray-800 d-inline-flex align-items-center me-2')
