from holoniq.utils import logging, log
from dash import html
import dash_holoniq_components as dhc

from dash_spa import spa, Blueprint
from dash_spa import SpaComponents

from app import create_dash
from server import serve_app

test = Blueprint('test')

@test.route('/page1')
def route1(ctx):

    btn = html.Button('Go to Page #2', id='btn', className="btn btn-primary btn-block")
    redirect = dhc.Location(id='redirect')

    @test.callback(redirect.output.pathname, [btn.input.n_clicks])
    def _cb(clicks):
        red = SpaComponents.NOUPDATE
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
def route2(ctx):

    btn = html.Button('Go to Page #1', id='btn', className="btn btn-primary btn-block")
    redirect = dhc.Location(id='redirect')

    @test.callback(redirect.output.pathname, [btn.input.n_clicks])
    def _cb(clicks):
        red = SpaComponents.NOUPDATE
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

    return app

#
# python -m examples.redirect
#


if __name__ == '__main__':
    app = create_app(create_dash)
    serve_app(app.dash,"/test/page1")
