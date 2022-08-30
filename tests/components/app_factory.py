from dash_spa.logging import log
from dash_spa import DashSPA, page_container, register_page

def single_page_app(page_layout):
    log.info('********************* create alert app *************************')
    app = DashSPA(__name__, pages_folder='')
    register_page('test', path='/', title="test", layout=page_layout())
    app.layout = page_container
    return app