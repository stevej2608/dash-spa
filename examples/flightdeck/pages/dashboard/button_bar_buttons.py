from dash_spa.components.dropdown_button_aoi import DropdownButtonAIO, dropdownLink

from ..icons.hero import ICON


def newTasksButton():
    return DropdownButtonAIO([
        dropdownLink("Add User", ICON.USER_ADD),
        dropdownLink("Add Widget", ICON.WIDGET),
        dropdownLink("Upload Files", ICON.UPLOAD),
        dropdownLink("Preview Security", ICON.SECURITY),
        dropdownLink("Upgrade to Pro", ICON.FIRE.ME2_DANGER),
    ], "New Task", buttonColor="gray-800")
