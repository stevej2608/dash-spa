from flask import request
from dash import html, dcc
from dash_spa import prefix, callback, session_context, SessionContext, session_data, component_id
from dash_spa.logging import log

from .icons import ARROW_ICON



class SidebarNavItem(html.Li):
    """Sidebar NavItem with 'active' added/removed from className when
    selected/deselected

    Note: For convenience item id's are globally allocated so only one sidebar is
    allowed in the application.
    """

    @staticmethod
    def is_active(href:str) -> bool:
        """Return true if given href is the currently active page

        Args:
            href (str): href is the currently active page

        Returns:
            bool: true if given href is the currently active page
        """

        try:
            return request.dash_pathname.startswith(href)
        except:
            return False


    def __init__(self, children, active, **_kwargs):

        className = _kwargs.pop('className', 'nav-item')

        if not 'nav-item' in className:
            className += ' nav-item'

        if active:
            className += ' active'

        super().__init__(children, className=className, **_kwargs)


def dropdownFolderEntry(text:str, href:str) -> html.Li:
    """Drop-down folder entry (decorated dcc.Link)

    Args:
        text (str): The link text
        href (str): the link href

    Returns:
        _type_: _description_
    """
    return SidebarNavItem([
        dcc.Link([
            html.Span(text, className='sidebar-text')
        ], className='nav-link', href=href)
    ], SidebarNavItem.is_active(href))


@session_data
class DropdownFolderContext(SessionContext):
    className: str = 'multi-level collapse'

class DropdownFolderAIO(html.Div):

    def __init__(self, children, text, icon, id=None):
        """Sidebar dropdown component with icon, text and arrow; that when clicked displays the child elements

        Args:
            children (list): The child elements
            text (str): The drop down text
            icon (Svg): The dropdown icon
            id (str): The component ID.
        """

        pid = prefix(id)
        state = session_context(DropdownFolderContext, id=pid('state'))

        # log.info('DropdownFolderAIO id=%s, state %s', id, state.className)

        button = html.Span([
            html.Span([
                html.Span(icon, className='sidebar-icon'),
                html.Span(text, className='sidebar-text')
            ]),
            html.Span(ARROW_ICON, className='link-arrow')
        ], id=pid('btn'), className='nav-link collapsed d-flex justify-content-between align-items-center')

        # Drop down container

        container = html.Div([
            html.Ul(children, className='flex-column nav')
        ], id=pid('container'), className=state.className, role='list')


        @callback(container.output.className, button.input.n_clicks, container.state.className)
        def update_dropdown(n_clicks, className):

            if not n_clicks:
                return className

            if 'collapse' in className:
                state.className = className.replace(' collapse', '')
            else:
                state.className = className + ' collapse'

            log.info('update_dropdown  id=%s, state %s', id, state.className)

            return state.className

        super().__init__(html.Li([button, container], className='nav-item'))
