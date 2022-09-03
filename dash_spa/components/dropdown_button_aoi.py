from dash import html, dcc
from .icons import DOWN_ARROW, PLUS
from .dropdown_aio import DropdownAIO

def dropdownLink(title, icon, href='#'):
    return dcc.Link([
        icon,
        title
    ], className='dropdown-item d-flex align-items-center', href=href)

class DropdownButtonAIO(DropdownAIO):

    """Button with supplied icon and down arrow. When clicked a drop-down
    selection of entries is revealed.

    Args:
        dropdownEntries (list): The dropdown entries
        buttonText (str): The button text
        buttonIcon (Svg, optional): Optional button icon. Defaults to PLUS.
        buttonColor (str, optional): BS5 button colour. Defaults to 'secondary'.
        downArrow (bool, optional): Show down arrow. Defaults to False.

    Example:

        DropdownButtonAIO([
            dropdownLink("Add User", USER_ADD),

            dropdownLink("Add Widget", WIDGET),

            dropdownLink("Upload Files", UPLOAD),

            dropdownLink("Preview Security", SECURITY),

            dropdownLink("Upgrade to Pro", FIRE_DANGER),

        ], "New Task", buttonColor="gray-800")

    """

    container_className = ''

    def __init__(self, dropdownEntries, buttonText, buttonIcon=PLUS,
                 buttonColor='secondary', downArrow=False, id=None):

        button = DropdownAIO.Button([
                buttonIcon,
                buttonText,
                DOWN_ARROW if downArrow else None
            ], className=self.button_className(buttonColor))

        # Drop down container

        container = html.Div(
            dropdownEntries,
            className=self.container_className)

        super().__init__(button, container, id=id)


    def button_className(self, buttonColor):
        return f'btn btn-{buttonColor}'
