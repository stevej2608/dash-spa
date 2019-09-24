from utils import logging, log
import dash_html_components as html

from dash_spa import spa, Blueprint
from app import app as dash_app

test = Blueprint('test')

@test.route('/page1')
def route1():
    spa = test.get_spa('page1')

    btn = spa.Button('Page #2', id='btn')
    redirect = spa.Redirect(id='redirect')

    @spa.callback(redirect.output.href, [btn.input.n_clicks])
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


    btn = spa.Button('Page #1', id='btn')
    redirect = spa.Redirect(id='redirect')

    @spa.callback(redirect.output.href, [btn.input.n_clicks])
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

def create_app():
    aps_log = logging.getLogger('werkzeug')
    aps_log.setLevel(logging.ERROR)

    app = spa.SinglePageApp(dash_app)
    app.register_blueprint(test, url_prefix='/test')

    return app

#
# python -m examples.redirect
#
# http://localhost:8050/test/page1
#

if __name__ == '__main__':
    print('\nvisit: http://localhost:8050/test/page1\n')
    app = create_app()
    app.run_server(debug=False, threaded=False)
