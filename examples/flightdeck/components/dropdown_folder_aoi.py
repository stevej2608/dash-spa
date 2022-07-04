from dash import html, dcc, callback, MATCH
from dash_spa import match, component_id

from icons.hero import ARROW_ICON

def dropdownFolderEntry(text, href):
    return html.Li([
        dcc.Link([
            html.Span(text, className='sidebar-text')
        ], className='nav-link', href=href)
    ], className='nav-item')

class DropdownFolderAIO(html.Div):

    class ids:
        button = match({'component': 'DropdownFolderAIO', 'subcomponent': 'button', 'idx': MATCH})
        container = match({'component': 'DropdownFolderAIO', 'subcomponent': 'container', 'idx': MATCH})

    # pylint: disable=no-self-argument

    @callback(ids.container.output.className, ids.button.input.n_clicks, ids.container.state.className)
    def update_dropdown(n_clicks, className):

        if not n_clicks:
            return className

        if 'collapse' in className:
            return className.replace(' collapse', '')
        else:
            return className + ' collapse'

    def __init__(self, children, text, icon, aio_id=None):
        """Sidebar dropdown component with icon, text and arrow; that when clicked displays the child elements

        Args:
            children (list): The child elements
            text (str): The drop down text
            icon (Svg): The dropdown icon
            aio_id (str, optional): The component ID. Defaults to None.
        """

        ids = DropdownFolderAIO.ids
        aio_id = aio_id if aio_id else component_id()

        button = html.Span([
            html.Span([
                html.Span(icon, className='sidebar-icon'),
                html.Span(text, className='sidebar-text')
            ]),
            html.Span(ARROW_ICON, className='link-arrow')
        ], id=ids.button.idx(aio_id), className='nav-link collapsed d-flex justify-content-between align-items-center')

        # Drop down container

        container = html.Div([
            html.Ul(children, className='flex-column nav')
        ], id=ids.container.idx(aio_id), className='multi-level collapse', role='list')

        super().__init__(html.Li([button, container], className='nav-item'))
