import dash
from dash import html
from dash_spa.logging import log
from dash_spa import spa_pages, NOUPDATE, page_container, register_page


from dash_spa.components.alert import Alert, SPA_ALERT


def single_page_app(page_layout):
    log.info('********************* create alert app *************************')
    app = dash.Dash(__name__,  plugins=[spa_pages])
    register_page(path='/', title="test", layout=page_layout())
    app.layout = page_container
    return app

def test_alert(dash_duo):

    # Create Dash UI and start the test server

    btn = None

    def layout():
        nonlocal btn

        btn = html.Button("Alert Button", id='alert_btn')

        @SPA_ALERT.update(btn.input.n_clicks)
        def btn_cb(clicks, store):
            if clicks:
                log.info('issue alert')
                alert = Alert("Basic alert", 'You clicked the button!')
                return alert.report()
            else:
                return NOUPDATE

        return html.Div([btn])

    app = single_page_app(layout)
    dash_duo.start_server(app)

    # Click a button to trigger the notify toast

    browser_btn = dash_duo.find_element(btn.css_id)
    browser_btn.click()

    result = dash_duo.wait_for_text_to_equal("#swal2-title", "Basic alert", timeout=3)
    assert result

    result = dash_duo.wait_for_text_to_equal("#swal2-html-container", "You clicked the button!", timeout=3)
    assert result
