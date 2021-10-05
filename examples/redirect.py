from holoniq.utils import logging, log
from dash import html

from dash_spa import spa, Blueprint

from app import create_dash
from server import serve_app

test = Blueprint('test')

@test.route('/page1')
def route1():
    spa = test.get_spa('page1')

    btn = spa.Button('Go to Page #2', id='btn')
    redirect = spa.Redirect(id='redirect')

    @spa.callback(redirect.output.pathname, [btn.input.n_clicks])
    def _cb(clicks):
        red = test.NOUPDATE
        log.info('btn clicks=%s', clicks)
        if clicks:
            red = test.url_for('page2')
        return red

    return html.Div([
        html.H2('Page #1'),
        btn,
        redirect
    ])


@test.route('/page2')
def route2():
    spa = test.get_spa('route2')

    btn = spa.Button('Go to Page #1', id='btn')
    redirect = spa.Redirect(id='redirect')

    @spa.callback(redirect.output.pathname, [btn.input.n_clicks])
    def _cb(clicks):
        red = test.NOUPDATE
        log.info('btn clicks=%s', clicks)
        if clicks:
            red = test.url_for('page1')
        return red

    return html.Div([
        html.H2('Page #2'),
        btn,
        redirect
    ])

def create_app(dash_factory):
    aps_log = logging.getLogger('werkzeug')
    aps_log.setLevel(logging.ERROR)

    app = spa.SinglePageApp(dash_factory)
    app.register_blueprint(test, url_prefix='/test')

    app.layout()

    return app.dash.server

#
# python -m examples.redirect
#


if __name__ == '__main__':
    app = create_app(create_dash)
    serve_app(app,"/test/page1")
