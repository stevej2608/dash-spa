from dash import html, dcc
from .icons import DOWN_ARROW_ICON, PLUS_ICON
from .dropdown_aio import DropdownAIO

def dropdownLink(title, icon, href='#'):
    return dcc.Link([
        icon,
        title
    ], className='dropdown-item d-flex align-items-center', href=href)

class DropdownButtonAIO(DropdownAIO):

    def __init__(self, dropdownEntries, buttonText, buttonIcon=PLUS_ICON, buttonColor='secondary', downArrow=False, id=None):
        """Button with supplied icon and down arrow. When clicked a drop-down
        selection of entries is revealed.

        Args:
            dropdownEntries (list): The dropdown entries
            buttonText (str): The button text
            buttonIcon (Svg, optional): Optional button icon. Defaults to PLUS_ICON.
            buttonColor (str, optional): BS5 button colour. Defaults to 'secondary'.
            downArrow (bool, optional): Show down arrow. Defaults to False.

        Example:

            DropdownButtonAIO([
                dropdownLink("Add User", USER_ADD_ICON),

                dropdownLink("Add Widget", WIDGET_ICON),

                dropdownLink("Upload Files", UPLOAD_ICON),

                dropdownLink("Preview Security", SECURITY_ICON),

                dropdownLink("Upgrade to Pro", FIRE_ICON_DANGER),

            ], "New Task", buttonColor="gray-800")

        """

        button = DropdownAIO.Button([
                buttonIcon,
                buttonText,
                DOWN_ARROW_ICON if downArrow else None
            ], className=f'btn btn-{buttonColor} d-inline-flex align-items-center me-2 dropdown-toggle')

        # Drop down container

        container = html.Div(
            dropdownEntries,
            className='dropdown-menu dashboard-dropdown dropdown-menu-start mt-2 py-1')

        super().__init__(button, container, id=id)