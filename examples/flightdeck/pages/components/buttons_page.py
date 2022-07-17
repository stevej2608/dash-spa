from copy import deepcopy
from pydoc import classname
from dash import html
import dash_bootstrap_components as dbc
from dash_svg import Svg, Path
from dash_spa import register_page, add_style
from ..common import breadCrumbs, banner, topNavBar, footer
from ..icons import FACEBOOK, TWITTER, YOUTUBE, GITHUB, PAYPAL, BEHANCE, DOWN_ARROW, DOWNLOAD

register_page(__name__, path="/pages/components/buttons", title="Dash/Flightdeck - Buttons")

FACEBOOK_TEXT_BTN = html.Button([FACEBOOK.ME2, "Login with Facebook"
    ], className='btn btn-facebook d-inline-flex align-items-center', type='button')

TWITTER_TEXT_BTN = html.Button([TWITTER.ME2, "Share on Twitter"
    ], className='btn btn-twitter text-white d-inline-flex align-items-center', type='button')

YOUTUBE_TEXT_BTN = html.Button([YOUTUBE.ME2, "Watch on YouTube"
    ], className='btn btn-youtube d-inline-flex align-items-center', type='button')

GITHUB_TEXT_BTN = html.Button([GITHUB.ME2, "Login with GitHub"
    ], className='btn btn-github d-inline-flex align-items-center', type='button')

PAYPAL_TEXT_BTN = html.Button([PAYPAL.ME2, "Donate with PayPal"
    ], className='btn btn-paypal d-inline-flex align-items-center', type='button')

BEHANCE_TEXT_BTN = html.Button([BEHANCE.ME2, "Follow us"
    ], className='btn btn-behance d-inline-flex align-items-center', type='button')


FACEBOOK_BTN = html.Button(FACEBOOK.XXS, className='btn btn-icon-only btn-facebook d-inline-flex align-items-center', type='button')

TWITTER_BTN = html.Button(TWITTER.XXS, className='btn btn-icon-only btn-twitter text-white d-inline-flex align-items-center', type='button')

YOUTUBE_BTN = html.Button(YOUTUBE.XXS, className='btn btn-icon-only btn-youtube d-inline-flex align-items-center', type='button')

GITHUB_BTN = html.Button(GITHUB.XXS, className='btn btn-icon-only btn-github d-inline-flex align-items-center', type='button')

PAYPAL_BTN = html.Button(PAYPAL.XXS, className='btn btn-icon-only btn-paypal d-inline-flex align-items-center', type='button')

BEHANCE_BTN = html.Button(BEHANCE.XXS, className='btn btn-icon-only btn-behance d-inline-flex align-items-center', type='button')



def TTButton(children, className, title, type, placement):
    # https://dash-bootstrap-components.opensource.faculty.ai/docs/components/tooltip/
    id=f"tooltip-target-{title.replace(' ', '-')}"

    if not isinstance(children, list):
        children = [children]

    children.append(dbc.Tooltip(title,  target=id, placement=placement))

    btn = html.Button(children, id=id, className=className, type=type)
    return btn


def PopoverButton(children, className, placement, content, trigger='legacy'):
    # https://dash-bootstrap-components.opensource.faculty.ai/docs/components/popover/
    id=f"popover-target-{content.replace(' ', '-')}"

    if not isinstance(children, list):
        children = [children]

    children.append(dbc.Popover(content,  body=True, target=id, placement=placement, trigger=trigger))

    btn = html.Button(children, id=id, className=className, type='button')
    return btn

WS = "\n"

def button_sizes():
    return  html.Div([
        html.Div(html.H2("Sizes", className='h5'), className='mb-3'),
        html.Button("Small", className='btn btn-sm btn-primary', type='button'),
        WS,
        html.Button("Regular", className='btn btn-primary', type='button'),
        WS,
        html.Button("Large Button", className='btn btn-lg btn-primary', type='button'),
    ])

# https://heroicons.com/

CLOUD_DOWNLOAD = Svg([
        Path(clipRule='evenodd', d='M2 9.5A3.5 3.5 0 005.5 13H9v2.586l-1.293-1.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L11 15.586V13h2.5a4.5 4.5 0 10-.616-8.958 4.002 4.002 0 10-7.753 1.977A3.5 3.5 0 002 9.5zm9 3.5H9V8a1 1 0 012 0v5z', fillRule='evenodd')
    ], className='icon icon-xxs ms-2', viewBox='0 0 20 20', fill="currentColor", xmlns='http://www.w3.org/2000/svg')


CHAT = Svg([
        Path(d='M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z',
             fillRule="evenodd", clipRule="evenodd")
    ], className='icon icon-xxs me-2', viewBox='0 0 20 20', fill="currentColor", xmlns='http://www.w3.org/2000/svg')


def button_with_icons():
    return  html.Div([
        html.Button(["Download", CLOUD_DOWNLOAD], className='btn btn-primary d-inline-flex align-items-center', type='button'),
        WS,
        html.Button([CHAT, "Contact Us" ], className='btn btn-primary d-inline-flex align-items-center', type='button'),
    ])


def dropdown_buttons():
    return  html.Div([

        html.H2("Dropdown buttons", className='h5 fw-bold mt-4 mb-3'),
        html.Div([

            # Offset dropdown

            html.Div([

                html.Button("Offset", className='btn btn-secondary dropdown-toggle', id='dropdownMenuOffset', type='button', **{"aria-expanded": "false", "data-bs-offset": "10,20", "data-bs-toggle": "dropdown"}),
                html.Ul([
                    html.Li([
                        html.A("Action", className='dropdown-item rounded-top', href='#')
                    ]),
                    html.Li([
                        html.A("Another action", className='dropdown-item', href='#')
                    ]),
                    html.Li([
                        html.A("Something else here", className='dropdown-item rounded-bottom', href='#')
                    ])
                ], className='dropdown-menu py-0', **{"aria-labelledby": "dropdownMenuOffset"})
            ], className='dropdown me-1'),

            # Reference dropdown

            html.Div([

                html.Button("Reference", className='btn btn-secondary', type='button'),
                html.Button([
                    DOWN_ARROW.XS,
                    html.Span("Toggle Dropdown", className='visually-hidden')
                ], className='btn btn-secondary dropdown-toggle dropdown-toggle-split', id='dropdownMenuReference', type='button', **{"aria-expanded": "false", "data-bs-reference": "parent", "data-bs-toggle": "dropdown"}),
                html.Ul([
                    html.Li([
                        html.A("Action", className='dropdown-item rounded-top', href='#')
                    ]),
                    html.Li([
                        html.A("Another action", className='dropdown-item', href='#')
                    ]),
                    html.Li([
                        html.A("Something else here", className='dropdown-item', href='#')
                    ]),
                    html.Li([
                        html.Hr(className='dropdown-divider')
                    ]),
                    html.Li([
                        html.A("Separated link", className='dropdown-item rounded-bottom', href='#')
                    ])
                ], className='dropdown-menu py-0', **{"aria-labelledby": "dropdownMenuReference"})

            ], className='btn-group'),


        ], className='d-flex'),

    ])


def link_buttons():
    return  html.Div([
        html.Div(html.H2("Link Buttons", className='h5'), className='mb-3 mt-5'),
        html.Div([
            html.A("Primary", className='text-default fw-bold me-3', href='#'),
            html.A([DOWNLOAD,"Icon Left"], className='text-primary d-inline-flex align-items-center me-3', href='#'),
            html.A(["Icon Right", DOWNLOAD], className='text-primary d-inline-flex align-items-center', href='#'),
        ], className="d-inline-flex align-items-center")
    ])


def tooltip_buttons():
    return  html.Div([
        html.Div(html.H2("Tooltips", className='h5'), className='mb-3 mt-5'),

        TTButton("Tooltip on top", className='btn btn-secondary', title='Tooltip on top', type='button', placement='top'),
        WS,
        TTButton("Tooltip on right", className='btn btn-secondary', title='Tooltip on right', type='button', placement='right'),
        WS,
        TTButton("Tooltip on bottom", className='btn btn-secondary', title='Tooltip on bottom', type='button', placement='bottom'),
        WS,
        TTButton("Tooltip on left", className='btn btn-secondary', title='Tooltip on left', type='button', placement='left'),
    ])


def popover_buttons():
    return  html.Div([

        html.Div(html.H2("Popovers", className='h5'), className='mb-3 mt-5'),

        PopoverButton("Popover on top", className='btn btn-secondary', placement="top", content="Top popover"),
        WS,
        PopoverButton("Popover on right", className='btn btn-secondary', placement="right", content="Right popover"),
        WS,
        PopoverButton("Popover on bottom", className='btn btn-secondary', placement="bottom", content="Bottom popover"),
        WS,
        PopoverButton("Popover on left", className='btn btn-secondary', placement="left", content="Left popover"),

    ])

def buttons_colours():
    return  html.Div([
        html.Div(html.H2("Choose your color", className='h5'), className='mb-3 mt-5'),

        html.Div(html.Small("Main", className='text-uppercase fw-bold'), className='mb-3 mt-5'),
        WS,
        html.Button("Primary", className='btn btn-primary', type='button'),
        WS,
        html.Button("Secondary", className='btn btn-secondary', type='button'),
        WS,
        html.Button("Tertiary", className='btn btn-tertiary', type='button'),
        WS,
        html.Button("Info", className='btn btn-info', type='button'),
        WS,
        html.Button("Success", className='btn btn-success', type='button'),
        WS,
        html.Button("Warning", className='btn btn-warning', type='button'),
        WS,
        html.Button("Danger", className='btn btn-danger', type='button'),
        WS,
        html.Button("Dark", className='btn btn-gray-800', type='button'),
        WS,
        html.Button("Gray", className='btn btn-gray-200', type='button'),
        WS,
        html.Button("Light", className='btn btn-gray-50', type='button'),
        WS,
        html.Button("White", className='btn btn-white', type='button'),

    ])


def button_outline():
    return  html.Div([
        html.Div(html.Small("Outline", className='text-uppercase fw-bold'), className='mb-3 mt-5'),

        WS,
        html.Button("Primary", className='btn btn-outline-primary', type='button'),
        WS,
        html.Button("Secondary", className='btn btn-outline-secondary', type='button'),
        WS,
        html.Button("Tertiary", className='btn btn-outline-tertiary', type='button'),
        WS,
        html.Button("Info", className='btn btn-outline-info', type='button'),
        WS,
        html.Button("Success", className='btn btn-outline-success', type='button'),
        WS,
        html.Button("Danger", className='btn btn-outline-danger', type='button'),
        WS,
        html.Button("Dark", className='btn btn-outline-gray-800', type='button'),
        WS,
        html.Button("Gray", className='btn btn-outline-gray-500', type='button'),

    ])


def button_rounded_outline():
    return  html.Div([

        html.Div(html.Small("Round Outline", className='text-uppercase fw-bold'), className='mb-3 mt-5'),

        html.Button("Primary", className='btn btn-pill btn-outline-primary', type='button'),
        WS,
        html.Button("Secondary", className='btn btn-pill btn-outline-secondary', type='button'),
        WS,
        html.Button("Tertiary", className='btn btn-pill btn-outline-tertiary', type='button'),
        WS,
        html.Button("Info", className='btn btn-pill btn-outline-info', type='button'),
        WS,
        html.Button("Success", className='btn btn-pill btn-outline-success', type='button'),
        WS,
        html.Button("Danger", className='btn btn-pill btn-outline-danger', type='button'),
        WS,
        html.Button("Dark", className='btn btn-pill btn-outline-gray-800', type='button'),
        WS,
        html.Button("Gray", className='btn btn-pill btn-outline-gray-500', type='button'),
    ])


def button_links():
    return  html.Div([
        html.Div(html.Small("Links", className='text-uppercase fw-bold'), className='mb-3 mt-5'),
        html.A("Default", className='text-default me-3', href='#'),
        WS,
        html.A("Primary", className='text-primary me-3', href='#'),
        WS,
        html.A("Secondary", className='text-secondary me-3', href='#'),
        WS,
        html.A("Tertiary", className='text-tertiary me-3', href='#'),
        WS,
        html.A("Info", className='text-info me-3', href='#'),
        WS,
        html.A("Success", className='text-success me-3', href='#'),
        WS,
        html.A("Danger", className='text-danger me-3', href='#'),
        WS,
        html.A("Dark", className='text-dark me-3', href='#'),
        WS,
        html.A("Gray", className='text-gray', href='#'),
    ])


def social_buttons():
    return  html.Div([
            html.Div([
                html.Div(html.H2("Social Buttons", className='h5 fw-bold'), className='mb-4 mt-5'),
                FACEBOOK_TEXT_BTN, html.Br(),
                TWITTER_TEXT_BTN, html.Br(),
                YOUTUBE_TEXT_BTN, html.Br(),
                GITHUB_TEXT_BTN, html.Br(),
                PAYPAL_TEXT_BTN, html.Br(),
                BEHANCE_TEXT_BTN
            ], className='col-lg-4 col-md-6'),

            html.Div([
                html.Div(html.H2("Only Icon", className='h5'), className='mb-4 mt-5'),
                FACEBOOK_BTN, html.Br(),
                TWITTER_BTN, html.Br(),
                YOUTUBE_BTN, html.Br(),
                GITHUB_BTN, html.Br(),
                PAYPAL_BTN, html.Br(),
                BEHANCE_BTN
                ], className='col-12 col-lg-6')
        ], className='row')


def buttons():

    return html.Div([
        html.Div([
            html.Div([
                html.Div([
                    button_sizes(),
                    button_with_icons(),
                    dropdown_buttons(),
                    link_buttons(),
                    tooltip_buttons(),
                    popover_buttons(),
                    buttons_colours(),
                    button_outline(),
                    button_rounded_outline(),
                    button_links(),
                    social_buttons()

                ], className='card-body')
            ], className='card border-light shadow-sm components-section')
        ], className='col-12 mb-4')
    ])

# Following is needed to make the tooltips align correctly with the
# associated button. The volt.css margin is 2rem which results in
# the tt being placed some distance away from the button
#
# https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.css

TOOLTIP_CSS_MIN = """
    .tooltip {
        margin: 0;
    }
"""

add_style(TOOLTIP_CSS_MIN)

layout =html.Main([
        topNavBar(),
        html.Div([
            breadCrumbs(["Components", "Buttons"]),
            banner("Buttons", 'https://themesberg.com/docs/volt-bootstrap-5-dashboard/components/buttons/')
        ], className='py-4'),
        buttons(),
        footer()
    ], className='content')
