from dash import html, dcc
from dash_svg import Svg, Path
from dash_spa import register_page
from ..common import breadCrumbs, banner, sideBar, mobileNavBar, topNavBar, footer

register_page(__name__, path="/pages/components/forms.html", title="Dash/Flightdeck - Forms")

def email():
    return  html.Div([
        html.Label("Email address", htmlFor='email'),
        dcc.Input(type='email', className='form-control', id='email'),
        html.Small("We'll never share your email with anyone else.", id='emailHelp', className='form-text text-muted')
    ], className='mb-4')


def left_icon():
    return  html.Div([
        html.Label("Icon Left", htmlFor='exampleInputIconLeft'),
        html.Div([
            html.Span([
                Svg([
                    Path(fillRule='evenodd', d='M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z', clipRule='evenodd')
                ], className='icon icon-xs text-gray-600', fill='currentColor', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg')
            ], className='input-group-text', id='basic-addon1'),
            dcc.Input(type='text', className='form-control', id='exampleInputIconLeft', placeholder='Search')
        ], className='input-group')
    ], className='mb-3')

def right_icon():
    return  html.Div([
        html.Label("Icon Right", htmlFor='exampleInputIconRight'),
        html.Div([
            dcc.Input(type='text', className='form-control', id='exampleInputIconRight', placeholder='Search'),
            html.Span([
                Svg([
                    Path(fillRule='evenodd', d='M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z', clipRule='evenodd')
                ], className='icon icon-xs text-gray-600', fill='currentColor', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg')
            ], className='input-group-text', id='basic-addon2')
        ], className='input-group')
    ], className='mb-3')

def password():
    return html.Div([
        html.Label("Password", htmlFor='exampleInputIconPassword'),
        html.Div([
            dcc.Input(type='password', className='form-control', id='exampleInputIconPassword', placeholder='Password'),
            html.Span([
                Svg([
                    Path(fillRule='evenodd', d='M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z', clipRule='evenodd')
                ], className='icon icon-xs text-gray-600', fill='currentColor', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg')
            ], className='input-group-text', id='basic-addon3')
        ], className='input-group')
    ], className='mb-3')


def first_name():
    return  html.Div([
        html.Label("First name", htmlFor='firstName'),
        dcc.Input(type='text', className='form-control is-valid', id='firstName', value='Mark', required=''),
        html.Div("Looks good!", className='valid-feedback')
    ], className='mb-3')

def text_area():
    return html.Div([
        html.Label("Example textarea", htmlFor='textarea'),
        html.Textarea(className='form-control', placeholder='Enter your message...', id='textarea', rows='4')
    ], className='my-4')


def user_name():
    return  html.Div([
        html.Label("Username", htmlFor='usernameValidate'),
        dcc.Input(type='text', className='form-control is-invalid', id='usernameValidate', required=''),
        html.Div("Please choose a username.", className='invalid-feedback')
    ], className='mb-4')


def birthday():
    # TODO: Calender popup
    return html.Div([
        html.Label("Birthday", htmlFor='birthday'),
        html.Div([
            html.Span([
                Svg([
                    Path(fillRule='evenodd', d='M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z', clipRule='evenodd')
                ], className='icon icon-xs text-gray-600', fill='currentColor', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg')
            ], className='input-group-text'),
            dcc.Input(className='form-control', id='birthday', type='text', placeholder='dd/mm/yyyy', required='')
        ], className='input-group')
    ], className='mb-3')

def disabled_input():
    return  html.Div([
        html.Label("Name", htmlFor='disabledTextInput'),
        dcc.Input(type='text', id='disabledTextInput', className='form-control', placeholder='Disabled input', disabled='')
    ], className='mb-3')


def disabled_select_menu():
    return html.Div([
        html.Label("Disabled select menu", htmlFor='disabledSelect'),
        html.Select([
            html.Option("Disabled select")
        ], id='disabledSelect', className='form-control', disabled='')
    ], className='mb-3')


def country():
    return  html.Div([
        html.Label("Country", className='my-1 me-2', htmlFor='country'),
        html.Select([
            html.Option("Open this select menu", selected=''),
            html.Option("One", value='1'),
            html.Option("Two", value='2'),
            html.Option("Three", value='3')
        ], className='form-select', id='country', **{"aria-label": "Default select example"})
    ], className='mb-4')

def file_input():
    return html.Div([
        html.Label("Default file input example", htmlFor='formFile', className='form-label'),
        dcc.Input(className='form-control', type='file', id='formFile')
    ], className='mb-3')


def checkboxes():
    return html.Div([
        html.Div([
            html.Span("Checkboxes Round", className='h6 fw-bold')
        ], className='mb-3'),
        html.Div([
            dcc.Input(className='form-check-input', type='checkbox', value='', id='defaultCheck10'),
            html.Label("Default checkbox", className='form-check-label', htmlFor='defaultCheck10')
        ], className='form-check'),
        html.Div([
            dcc.Input(className='form-check-input', type='checkbox', value='', id='defaultCheck20', disabled=''),
            html.Label("Disabled checkbox", className='form-check-label', htmlFor='defaultCheck20')
        ], className='form-check')
    ], className='col-lg-3 col-md-6')


def radio():
    return  html.Div([
        html.Fieldset([
            html.Legend("Radios", className='h6'),
            html.Div([
                dcc.Input(className='form-check-input', type='radio', name='exampleRadios', id='exampleRadios1', value='option1'),
                html.Label("Default radio", className='form-check-label', htmlFor='exampleRadios1')
            ], className='form-check'),
            html.Div([
                dcc.Input(className='form-check-input', type='radio', name='exampleRadios', id='exampleRadios2', value='option2'),
                html.Label("Second default radio", className='form-check-label', htmlFor='exampleRadios2')
            ], className='form-check'),
            html.Div([
                dcc.Input(className='form-check-input', type='radio', name='exampleRadios', id='exampleRadios3', value='option3', disabled=''),
                html.Label("Disabled radio", className='form-check-label', htmlFor='exampleRadios3')
            ], className='form-check'),
            # End of Radio
        ])
    ], className='col-lg-3 col-sm-6 mt-4 mt-md-0')

def switches():
    return html.Div([
        html.Div([
            html.Span("Switches", className='h6 fw-bold')
        ], className='mb-3'),
        html.Div([
            dcc.Input(className='form-check-input', type='checkbox', id='flexSwitchCheckDefault'),
            html.Label("Default switch input", className='form-check-label', htmlFor='flexSwitchCheckDefault')
        ], className='form-check form-switch'),
        html.Div([
            dcc.Input(className='form-check-input', type='checkbox', id='flexSwitchCheckChecked'),
            html.Label("Checked switch input", className='form-check-label', htmlFor='flexSwitchCheckChecked')
        ], className='form-check form-switch'),
        html.Div([
            dcc.Input(className='form-check-input', type='checkbox', id='flexSwitchCheckDisabled', disabled=''),
            html.Label("Disabled switch input", className='form-check-label', htmlFor='flexSwitchCheckDisabled')
        ], className='form-check form-switch'),
        html.Div([
            dcc.Input(className='form-check-input', type='checkbox', id='flexSwitchCheckCheckedDisabled', disabled=''),
            html.Label("Disabled checked switch input", className='form-check-label', htmlFor='flexSwitchCheckCheckedDisabled')
        ], className='form-check form-switch')
    ], className='col-lg-3 col-sm-6 mt-4 mt-md-0')

def forms():
    return html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            email(),
                            left_icon(),
                            right_icon(),
                            password(),
                            first_name()
                        ], className='col-lg-4 col-sm-6'),
                        html.Div([
                            text_area(),
                            user_name(),
                        ], className='col-lg-4 col-sm-6'),
                        html.Div([
                            birthday(),
                            disabled_input(),
                            disabled_select_menu(),
                            file_input()
                        ], className='col-lg-4 col-sm-6')
                    ], className='row mb-4'),
                    html.Div([
                        checkboxes(),
                        radio(),
                        switches()
                    ], className='row mb-5 mb-lg-5')
                ], className='card-body')
            ], className='card border-0 shadow components-section')
        ], className='col-12 mb-4')
    ], className='row')

layout = html.Div([
        mobileNavBar(),
        sideBar(),
        html.Main([
            topNavBar(),
            html.Div([
                breadCrumbs(["Components", "Forms"]),
                banner("Forms", 'https://themesberg.com/docs/volt-bootstrap-5-dashboard/components/forms/')
            ], className='py-4'),
            forms(),
            footer()
        ], className='content')
    ])