
from dash_spa.components.dropdown_button_aoi import DropdownButtonAIO, dropdownLink

from ..icons.hero import USER_ADD_ICON, WIDGET_ICON, UPLOAD_ICON, SECURITY_ICON, FIRE_ICON_DANGER


def newTasksButton():
    return DropdownButtonAIO([
        dropdownLink("Add User", USER_ADD_ICON),
        dropdownLink("Add Widget", WIDGET_ICON),
        dropdownLink("Upload Files", UPLOAD_ICON),
        dropdownLink("Preview Security", SECURITY_ICON),
        dropdownLink("Upgrade to Pro", FIRE_ICON_DANGER),
    ], "New Task", buttonColor="gray-800")
