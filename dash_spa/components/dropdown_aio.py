import time
from dash import html, MATCH
from dash.development.base_component import Component
import dash_holoniq_components as dhc

from dash_spa import callback
from dash_spa.logging import log

from dash_prefix import prefix

class DropdownAIO(html.Div):
    """Button and container. The container is shown when the
    button is clicked. The container is hidden when focus is lost.

    The button **must** be a DropdownAIO.Button


    Args:
        button (dhc.Button): Button, when clicked displays the container
        container (Component): Container to be shown/hidden
        aio_id (str, optional): The container prefix. If None one will be allocated.
    """

    Button = dhc.Button


    def __init__(self, button:dhc.Button, container:Component, id, classname_modifier='show'):

        pid = prefix(id)

        # log.info('DropdownAIO pid=%s', id)

        button.id = pid('btn')
        container.id = pid('container')

        @callback(container.output.className, button.input.n_clicks,
                  button.input.focus, button.state.id, container.state.className,
                  prevent_initial_call=True
                  )
        def show_dropdown(button_clicks, button_focus, id, className):

            # log.info('%s button_clicks=%s, button_focus=%s',id, button_clicks, button_focus)

            if not button_clicks:
                return className

            classNames = className.split()

            if classname_modifier in classNames:
                if button_focus is False:
                    classNames.remove(classname_modifier)

                    # Delay hiding the container. If we don't do this click
                    # event from elements in the container are lost
                    # TODO: Add a configurable delay to dhc.Button

                    time.sleep(300/1000)
            else:
                classNames.append(classname_modifier)

            className = ' '.join(classNames)

            #log.info("DropdownAIO className='%s'", className)

            return className






        super().__init__(html.Div([button, container], className='dropdown'))
