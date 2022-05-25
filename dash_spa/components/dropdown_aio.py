import time
from dash import html, callback, MATCH
from dash.development.base_component import Component
import dash_holoniq_components as dhc
from dash_spa.logging import log

from dash_prefix import match, component_id

class DropdownAIO(html.Div):
    """Button and container. The container is shown when the
    button is clicked. The container is hidden when focus is lost.

    The button **must** be a dash_holoniq_components Button


    Args:
        button (dhc.Button): Button, when clicked displays the container
        container (Component): Container to be shown/hidden
        aio_id (str, optional): The container prefix. If None one will be allocated.
    """

    Button = dhc.Button

    class ids:
        button = match({'component': 'DropdownAIO', 'subcomponent': 'button', 'idx': MATCH})
        container = match({'component': 'DropdownIO', 'subcomponent': 'container', 'idx': MATCH})

    # pylint: disable=no-self-argument

    @callback(ids.container.output.className, ids.button.input.n_clicks, ids.button.input.focus, ids.container.state.className)
    def show_dropdown(button_clicks, button_focus, className):

        if not button_clicks:
            return className

        classNames = className.split()

        if 'show' in classNames:
            if button_focus is False:
                classNames.remove('show')

                # Delay hiding the container. If we don't do this click
                # event from elements in the container are lost
                # TODO: Add a configurable delay to dhc.Button

                time.sleep(300/1000)
        else:
            classNames.append('show')

        className = ' '.join(classNames)

        #log.info("DropdownAIO className='%s'", className)

        return className


    def __init__(self, button:dhc.Button, container:Component, aio_id=None):

        ids = DropdownAIO.ids
        aio_id = aio_id if aio_id else component_id()

        # logging.info('DropdownAIO pid=%s', aio_id)

        button.id = ids.button.idx(aio_id)
        container.id = ids.container.idx(aio_id)

        super().__init__(html.Div([button, container], className='dropdown'))
