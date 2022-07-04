from dash import html

from components.dropdown_button_aoi import DropdownButtonAIO, dropdownLink
from icons.hero import DOCUMENT_ICON, MESSAGE_ICON, UPLOAD_ICON, FIRE_ICON_DANGER, CALENDER_ICON

def newButton():
    return DropdownButtonAIO([
        dropdownLink("Document", DOCUMENT_ICON),
        dropdownLink("Message", MESSAGE_ICON),
        dropdownLink("Product", UPLOAD_ICON),
        dropdownLink("My Plan", FIRE_ICON_DANGER),
    ], "New")

def calenderButton():
    return  html.Button([
        CALENDER_ICON
    ], type='button', className='btn btn-gray-800 d-inline-flex align-items-center me-2')
