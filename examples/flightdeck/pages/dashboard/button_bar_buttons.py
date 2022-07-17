
from dash_spa.components.dropdown_button_aoi import DropdownButtonAIO, dropdownLink

from ..icons.hero import USER_ADD, WIDGET, UPLOAD, SECURITY, FIRE_DANGER


def newTasksButton():
    return DropdownButtonAIO([
        dropdownLink("Add User", USER_ADD),
        dropdownLink("Add Widget", WIDGET),
        dropdownLink("Upload Files", UPLOAD),
        dropdownLink("Preview Security", SECURITY),
        dropdownLink("Upgrade to Pro", FIRE_DANGER),
    ], "New Task", buttonColor="gray-800")
