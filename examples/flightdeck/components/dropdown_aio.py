import logging
from dash import html, callback, MATCH
from dash.development.base_component import Component
import dash_holoniq_components as dhc
from dash_spa import match, component_id

class DropdownAIO(html.Div):

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
        else:
            classNames.append('show')

        return ' '.join(classNames)


    def __init__(self, button:Component, container:Component, aio_id=None):

        ids = DropdownAIO.ids
        aio_id = aio_id if aio_id else component_id()

        # logging.info('DropdownAIO pid=%s', aio_id)

        button.id = ids.button.idx(aio_id)
        container.id = ids.container.idx(aio_id)

        super().__init__(html.Div([button, container], className='dropdown'))
