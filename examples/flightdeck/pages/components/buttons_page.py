from dash import html
from dash_svg import Svg, Path
from dash_spa import register_page
from ..icons.hero import HOME_ICON
from ..common import sideBar, mobileNavBar, topNavBar, footer

register_page(__name__, path="/pages/components/buttons.html", title="Dash/Flightdeck - Buttons")

def breadCrumbs():
    return  html.Nav([
        html.Ol([
            html.Li([
                html.A([
                    HOME_ICON
                ], href='#')
            ], className='breadcrumb-item'),
            html.Li([
                html.A("Components", href='#')
            ], className='breadcrumb-item'),
            html.Li("Buttons", className='breadcrumb-item active', **{"aria-current": "page"})
        ], className='breadcrumb breadcrumb-dark breadcrumb-transparent')
    ], className='d-none d-md-inline-block', **{"aria-label": "breadcrumb"})


def banner():
    return html.Div([
        html.Div([
            html.H1("Buttons", className='h4'),
            html.P("Dozens of reusable components built to provide buttons, alerts, popovers, and more.", className='mb-0')
        ], className='mb-3 mb-lg-0'),
        html.Div([
            html.A([
                html.I(className='far fa-question-circle me-1'),
                "Buttons Docs"
            ], href='https://themesberg.com/docs/volt-bootstrap-5-dashboard/components/buttons/', className='btn btn-outline-gray')
        ])
    ], className='d-flex justify-content-between w-100 flex-wrap')


FACEBOOK_TEXT_BTN = html.Button([
        Svg([
            Path(d='M279.14 288l14.22-92.66h-88.91v-60.13c0-25.35 12.42-50.06 52.24-50.06h40.42V6.26S260.43 0 225.36 0c-73.22 0-121.08 44.38-121.08 124.72v70.62H22.89V288h81.39v224h100.17V288z', fill='currentColor')
        ], className='icon icon-xxs me-2', role='img', viewBox='0 0 320 512', xmlns='http://www.w3.org/2000/svg', **{"aria-hidden": "true", "data-icon": "facebook-f", "data-prefix": "fab"}),
        "Login with Facebook"
    ], className='btn btn-facebook d-inline-flex align-items-center', type='button')

TWITTER_TEXT_BTN = html.Button([
        Svg([
            Path(d='M459.37 151.716c.325 4.548.325 9.097.325 13.645 0 138.72-105.583 298.558-298.558 298.558-59.452 0-114.68-17.219-161.137-47.106 8.447.974 16.568 1.299 25.34 1.299 49.055 0 94.213-16.568 130.274-44.832-46.132-.975-84.792-31.188-98.112-72.772 6.498.974 12.995 1.624 19.818 1.624 9.421 0 18.843-1.3 27.614-3.573-48.081-9.747-84.143-51.98-84.143-102.985v-1.299c13.969 7.797 30.214 12.67 47.431 13.319-28.264-18.843-46.781-51.005-46.781-87.391 0-19.492 5.197-37.36 14.294-52.954 51.655 63.675 129.3 105.258 216.365 109.807-1.624-7.797-2.599-15.918-2.599-24.04 0-57.828 46.782-104.934 104.934-104.934 30.213 0 57.502 12.67 76.67 33.137 23.715-4.548 46.456-13.32 66.599-25.34-7.798 24.366-24.366 44.833-46.132 57.827 21.117-2.273 41.584-8.122 60.426-16.243-14.292 20.791-32.161 39.308-52.628 54.253z', fill='currentColor')
        ], className='icon icon-xxs me-2', role='img', viewBox='0 0 512 512', xmlns='http://www.w3.org/2000/svg', **{"aria-hidden": "true", "data-icon": "twitter", "data-prefix": "fab"}),
        "Share on Twitter"
    ], className='btn btn-twitter text-white d-inline-flex align-items-center', type='button')

YOUTUBE_TEXT_BTN = html.Button([
        Svg([
            Path(d='M549.655 124.083c-6.281-23.65-24.787-42.276-48.284-48.597C458.781 64 288 64 288 64S117.22 64 74.629 75.486c-23.497 6.322-42.003 24.947-48.284 48.597-11.412 42.867-11.412 132.305-11.412 132.305s0 89.438 11.412 132.305c6.281 23.65 24.787 41.5 48.284 47.821C117.22 448 288 448 288 448s170.78 0 213.371-11.486c23.497-6.321 42.003-24.171 48.284-47.821 11.412-42.867 11.412-132.305 11.412-132.305s0-89.438-11.412-132.305zm-317.51 213.508V175.185l142.739 81.205-142.739 81.201z', fill='currentColor')
        ], className='icon icon-xxs me-2', role='img', viewBox='0 0 576 512', xmlns='http://www.w3.org/2000/svg', **{"aria-hidden": "true", "data-icon": "youtube", "data-prefix": "fab"}),
        "Watch on YouTube"
    ], className='btn btn-youtube d-inline-flex align-items-center', type='button')

GITHUB_TEXT_BTN = html.Button([
        Svg([
            Path(d='M165.9 397.4c0 2-2.3 3.6-5.2 3.6-3.3.3-5.6-1.3-5.6-3.6 0-2 2.3-3.6 5.2-3.6 3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9 2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5.3-6.2 2.3zm44.2-1.7c-2.9.7-4.9 2.6-4.6 4.9.3 2 2.9 3.3 5.9 2.6 2.9-.7 4.9-2.6 4.6-4.6-.3-1.9-3-3.2-5.9-2.9zM244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2 12.8 2.3 17.3-5.6 17.3-12.1 0-6.2-.3-40.4-.3-61.4 0 0-70 15-84.7-29.8 0 0-11.4-29.1-27.8-36.6 0 0-22.9-15.7 1.6-15.4 0 0 24.9 2 38.6 25.8 21.9 38.6 58.6 27.5 72.9 20.9 2.3-16 8.8-27.1 16-33.7-55.9-6.2-112.3-14.3-112.3-110.5 0-27.5 7.6-41.3 23.6-58.9-2.6-6.5-11.1-33.3 2.6-67.9 20.9-6.5 69 27 69 27 20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27 13.7 34.7 5.2 61.4 2.6 67.9 16 17.7 25.8 31.5 25.8 58.9 0 96.5-58.9 104.2-114.8 110.5 9.2 7.9 17 22.9 17 46.4 0 33.7-.3 75.4-.3 83.6 0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252 496 113.3 383.5 8 244.8 8zM97.2 352.9c-1.3 1-1 3.3.7 5.2 1.6 1.6 3.9 2.3 5.2 1 1.3-1 1-3.3-.7-5.2-1.6-1.6-3.9-2.3-5.2-1zm-10.8-8.1c-.7 1.3.3 2.9 2.3 3.9 1.6 1 3.6.7 4.3-.7.7-1.3-.3-2.9-2.3-3.9-2-.6-3.6-.3-4.3.7zm32.4 35.6c-1.6 1.3-1 4.3 1.3 6.2 2.3 2.3 5.2 2.6 6.5 1 1.3-1.3.7-4.3-1.3-6.2-2.2-2.3-5.2-2.6-6.5-1zm-11.4-14.7c-1.6 1-1.6 3.6 0 5.9 1.6 2.3 4.3 3.3 5.6 2.3 1.6-1.3 1.6-3.9 0-6.2-1.4-2.3-4-3.3-5.6-2z', fill='currentColor')
        ], className='icon icon-xxs me-2', role='img', viewBox='0 0 496 512', xmlns='http://www.w3.org/2000/svg', **{"aria-hidden": "true", "data-icon": "github", "data-prefix": "fab"}),
        "Login with GitHub"
    ], className='btn btn-github d-inline-flex align-items-center', type='button')

PAYPAL_TEXT_BTN = html.Button([
        Svg([
            Path(d='M111.4 295.9c-3.5 19.2-17.4 108.7-21.5 134-.3 1.8-1 2.5-3 2.5H12.3c-7.6 0-13.1-6.6-12.1-13.9L58.8 46.6c1.5-9.6 10.1-16.9 20-16.9 152.3 0 165.1-3.7 204 11.4 60.1 23.3 65.6 79.5 44 140.3-21.5 62.6-72.5 89.5-140.1 90.3-43.4.7-69.5-7-75.3 24.2zM357.1 152c-1.8-1.3-2.5-1.8-3 1.3-2 11.4-5.1 22.5-8.8 33.6-39.9 113.8-150.5 103.9-204.5 103.9-6.1 0-10.1 3.3-10.9 9.4-22.6 140.4-27.1 169.7-27.1 169.7-1 7.1 3.5 12.9 10.6 12.9h63.5c8.6 0 15.7-6.3 17.4-14.9.7-5.4-1.1 6.1 14.4-91.3 4.6-22 14.3-19.7 29.3-19.7 71 0 126.4-28.8 142.9-112.3 6.5-34.8 4.6-71.4-23.8-92.6z', fill='currentColor')
        ], className='icon icon-xxs me-2', role='img', viewBox='0 0 384 512', xmlns='http://www.w3.org/2000/svg', **{"aria-hidden": "true", "data-icon": "paypal", "data-prefix": "fab"}),
        "Donate with PayPal"
    ], className='btn btn-paypal d-inline-flex align-items-center', type='button')

FOLLOW_US_TEXT_BTN = html.Button([
        Svg([
            Path(d='M232 237.2c31.8-15.2 48.4-38.2 48.4-74 0-70.6-52.6-87.8-113.3-87.8H0v354.4h171.8c64.4 0 124.9-30.9 124.9-102.9 0-44.5-21.1-77.4-64.7-89.7zM77.9 135.9H151c28.1 0 53.4 7.9 53.4 40.5 0 30.1-19.7 42.2-47.5 42.2h-79v-82.7zm83.3 233.7H77.9V272h84.9c34.3 0 56 14.3 56 50.6 0 35.8-25.9 47-57.6 47zm358.5-240.7H376V94h143.7v34.9zM576 305.2c0-75.9-44.4-139.2-124.9-139.2-78.2 0-131.3 58.8-131.3 135.8 0 79.9 50.3 134.7 131.3 134.7 61.3 0 101-27.6 120.1-86.3H509c-6.7 21.9-34.3 33.5-55.7 33.5-41.3 0-63-24.2-63-65.3h185.1c.3-4.2.6-8.7.6-13.2zM390.4 274c2.3-33.7 24.7-54.8 58.5-54.8 35.4 0 53.2 20.8 56.2 54.8H390.4z', fill='currentColor')
        ], className='icon icon-xxs me-2', role='img', viewBox='0 0 576 512', xmlns='http://www.w3.org/2000/svg', **{"aria-hidden": "true", "data-icon": "behance", "data-prefix": "fab"}),
        "Follow us"
    ], className='btn btn-behance d-inline-flex align-items-center', type='button')


FACEBOOK_BTN = html.Button([
        Svg([
            Path(d='M279.14 288l14.22-92.66h-88.91v-60.13c0-25.35 12.42-50.06 52.24-50.06h40.42V6.26S260.43 0 225.36 0c-73.22 0-121.08 44.38-121.08 124.72v70.62H22.89V288h81.39v224h100.17V288z', fill='currentColor')
        ], className='icon icon-xxs', role='img', viewBox='0 0 320 512', xmlns='http://www.w3.org/2000/svg', **{"aria-hidden": "true", "data-icon": "facebook-f", "data-prefix": "fab"})
    ], className='btn btn-icon-only btn-facebook d-inline-flex align-items-center', type='button')

TWITTER_BTN = html.Button([
        Svg([
            Path(d='M459.37 151.716c.325 4.548.325 9.097.325 13.645 0 138.72-105.583 298.558-298.558 298.558-59.452 0-114.68-17.219-161.137-47.106 8.447.974 16.568 1.299 25.34 1.299 49.055 0 94.213-16.568 130.274-44.832-46.132-.975-84.792-31.188-98.112-72.772 6.498.974 12.995 1.624 19.818 1.624 9.421 0 18.843-1.3 27.614-3.573-48.081-9.747-84.143-51.98-84.143-102.985v-1.299c13.969 7.797 30.214 12.67 47.431 13.319-28.264-18.843-46.781-51.005-46.781-87.391 0-19.492 5.197-37.36 14.294-52.954 51.655 63.675 129.3 105.258 216.365 109.807-1.624-7.797-2.599-15.918-2.599-24.04 0-57.828 46.782-104.934 104.934-104.934 30.213 0 57.502 12.67 76.67 33.137 23.715-4.548 46.456-13.32 66.599-25.34-7.798 24.366-24.366 44.833-46.132 57.827 21.117-2.273 41.584-8.122 60.426-16.243-14.292 20.791-32.161 39.308-52.628 54.253z', fill='currentColor')
        ], className='icon icon-xxs', role='img', viewBox='0 0 512 512', xmlns='http://www.w3.org/2000/svg', **{"aria-hidden": "true", "data-icon": "twitter", "data-prefix": "fab"})
    ], className='btn btn-icon-only btn-twitter text-white d-inline-flex align-items-center', type='button')

YOUTUBE_BTN = html.Button([
        Svg([
            Path(d='M549.655 124.083c-6.281-23.65-24.787-42.276-48.284-48.597C458.781 64 288 64 288 64S117.22 64 74.629 75.486c-23.497 6.322-42.003 24.947-48.284 48.597-11.412 42.867-11.412 132.305-11.412 132.305s0 89.438 11.412 132.305c6.281 23.65 24.787 41.5 48.284 47.821C117.22 448 288 448 288 448s170.78 0 213.371-11.486c23.497-6.321 42.003-24.171 48.284-47.821 11.412-42.867 11.412-132.305 11.412-132.305s0-89.438-11.412-132.305zm-317.51 213.508V175.185l142.739 81.205-142.739 81.201z', fill='currentColor')
        ], className='icon icon-xxs', role='img', viewBox='0 0 576 512', xmlns='http://www.w3.org/2000/svg', **{"aria-hidden": "true", "data-icon": "youtube", "data-prefix": "fab"})
    ], className='btn btn-icon-only btn-youtube d-inline-flex align-items-center', type='button')

GITHUB_BTN = html.Button([
        Svg([
            Path(d='M165.9 397.4c0 2-2.3 3.6-5.2 3.6-3.3.3-5.6-1.3-5.6-3.6 0-2 2.3-3.6 5.2-3.6 3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9 2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5.3-6.2 2.3zm44.2-1.7c-2.9.7-4.9 2.6-4.6 4.9.3 2 2.9 3.3 5.9 2.6 2.9-.7 4.9-2.6 4.6-4.6-.3-1.9-3-3.2-5.9-2.9zM244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2 12.8 2.3 17.3-5.6 17.3-12.1 0-6.2-.3-40.4-.3-61.4 0 0-70 15-84.7-29.8 0 0-11.4-29.1-27.8-36.6 0 0-22.9-15.7 1.6-15.4 0 0 24.9 2 38.6 25.8 21.9 38.6 58.6 27.5 72.9 20.9 2.3-16 8.8-27.1 16-33.7-55.9-6.2-112.3-14.3-112.3-110.5 0-27.5 7.6-41.3 23.6-58.9-2.6-6.5-11.1-33.3 2.6-67.9 20.9-6.5 69 27 69 27 20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27 13.7 34.7 5.2 61.4 2.6 67.9 16 17.7 25.8 31.5 25.8 58.9 0 96.5-58.9 104.2-114.8 110.5 9.2 7.9 17 22.9 17 46.4 0 33.7-.3 75.4-.3 83.6 0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252 496 113.3 383.5 8 244.8 8zM97.2 352.9c-1.3 1-1 3.3.7 5.2 1.6 1.6 3.9 2.3 5.2 1 1.3-1 1-3.3-.7-5.2-1.6-1.6-3.9-2.3-5.2-1zm-10.8-8.1c-.7 1.3.3 2.9 2.3 3.9 1.6 1 3.6.7 4.3-.7.7-1.3-.3-2.9-2.3-3.9-2-.6-3.6-.3-4.3.7zm32.4 35.6c-1.6 1.3-1 4.3 1.3 6.2 2.3 2.3 5.2 2.6 6.5 1 1.3-1.3.7-4.3-1.3-6.2-2.2-2.3-5.2-2.6-6.5-1zm-11.4-14.7c-1.6 1-1.6 3.6 0 5.9 1.6 2.3 4.3 3.3 5.6 2.3 1.6-1.3 1.6-3.9 0-6.2-1.4-2.3-4-3.3-5.6-2z', fill='currentColor')
        ], className='icon icon-xxs', role='img', viewBox='0 0 496 512', xmlns='http://www.w3.org/2000/svg', **{"aria-hidden": "true", "data-icon": "github", "data-prefix": "fab"})
    ], className='btn btn-icon-only btn-github d-inline-flex align-items-center', type='button')

PAYPAL_BTN = html.Button([
        Svg([
            Path(d='M111.4 295.9c-3.5 19.2-17.4 108.7-21.5 134-.3 1.8-1 2.5-3 2.5H12.3c-7.6 0-13.1-6.6-12.1-13.9L58.8 46.6c1.5-9.6 10.1-16.9 20-16.9 152.3 0 165.1-3.7 204 11.4 60.1 23.3 65.6 79.5 44 140.3-21.5 62.6-72.5 89.5-140.1 90.3-43.4.7-69.5-7-75.3 24.2zM357.1 152c-1.8-1.3-2.5-1.8-3 1.3-2 11.4-5.1 22.5-8.8 33.6-39.9 113.8-150.5 103.9-204.5 103.9-6.1 0-10.1 3.3-10.9 9.4-22.6 140.4-27.1 169.7-27.1 169.7-1 7.1 3.5 12.9 10.6 12.9h63.5c8.6 0 15.7-6.3 17.4-14.9.7-5.4-1.1 6.1 14.4-91.3 4.6-22 14.3-19.7 29.3-19.7 71 0 126.4-28.8 142.9-112.3 6.5-34.8 4.6-71.4-23.8-92.6z', fill='currentColor')
        ], className='icon icon-xxs', role='img', viewBox='0 0 384 512', xmlns='http://www.w3.org/2000/svg', **{"aria-hidden": "true", "data-icon": "paypal", "data-prefix": "fab"})
    ], className='btn btn-icon-only btn-paypal d-inline-flex align-items-center', type='button')

FOLLOW_US_BTN = html.Button([
        Svg([
            Path(d='M232 237.2c31.8-15.2 48.4-38.2 48.4-74 0-70.6-52.6-87.8-113.3-87.8H0v354.4h171.8c64.4 0 124.9-30.9 124.9-102.9 0-44.5-21.1-77.4-64.7-89.7zM77.9 135.9H151c28.1 0 53.4 7.9 53.4 40.5 0 30.1-19.7 42.2-47.5 42.2h-79v-82.7zm83.3 233.7H77.9V272h84.9c34.3 0 56 14.3 56 50.6 0 35.8-25.9 47-57.6 47zm358.5-240.7H376V94h143.7v34.9zM576 305.2c0-75.9-44.4-139.2-124.9-139.2-78.2 0-131.3 58.8-131.3 135.8 0 79.9 50.3 134.7 131.3 134.7 61.3 0 101-27.6 120.1-86.3H509c-6.7 21.9-34.3 33.5-55.7 33.5-41.3 0-63-24.2-63-65.3h185.1c.3-4.2.6-8.7.6-13.2zM390.4 274c2.3-33.7 24.7-54.8 58.5-54.8 35.4 0 53.2 20.8 56.2 54.8H390.4z', fill='currentColor')
        ], className='icon icon-xxs', role='img', viewBox='0 0 576 512', xmlns='http://www.w3.org/2000/svg', **{"aria-hidden": "true", "data-icon": "behance", "data-prefix": "fab"})
    ], className='btn btn-icon-only btn-behance d-inline-flex align-items-center', type='button')


def buttons():
    return html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Div(html.H2("Sizes", className='h5'), className='mb-3'),
                    html.Button("Small", className='btn btn-sm btn-primary', type='button'),
                    html.Button("Regular", className='btn btn-primary', type='button'),
                    html.Button("Large Button", className='btn btn-lg btn-primary', type='button'),

                    html.H2("With Icons", className='h5 fw-bold mt-4 mb-3'),

                    html.Button([
                        "Download",
                        Svg([
                            Path(clipRule='evenodd', d='M2 9.5A3.5 3.5 0 005.5 13H9v2.586l-1.293-1.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L11 15.586V13h2.5a4.5 4.5 0 10-.616-8.958 4.002 4.002 0 10-7.753 1.977A3.5 3.5 0 002 9.5zm9 3.5H9V8a1 1 0 012 0v5z', fillRule='evenodd')
                        ], className='icon icon-xxs ms-2', viewBox='0 0 20 20', fill="currentColor", xmlns='http://www.w3.org/2000/svg')
                    ], className='btn btn-primary d-inline-flex align-items-center', type='button'),

                    html.Button([
                        Svg([
                            Path(d='M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z', strokeLinecap='round', strokeLinejoin='round', strokeWidth='2')
                        ], className='icon icon-xxs me-2', viewBox='0 0 24 24', fill="none", xmlns='http://www.w3.org/2000/svg'),
                        "Contact Us"
                    ], className='btn btn-primary d-inline-flex align-items-center', type='button'),

                    html.H2("Dropdown buttons", className='h5 fw-bold mt-4 mb-3'),
                    html.Div([
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
                        html.Div([
                            html.Button("Reference", className='btn btn-secondary', type='button'),
                            html.Button([
                                Svg([
                                    Path(clipRule='evenodd', d='M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z', fillRule='evenodd')
                                ], className='icon icon-xs', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg'),
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
                        ], className='btn-group')
                    ], className='d-flex'),

                    html.Div(html.H2("Link Buttons", className='h5'), className='mb-3 mt-5'),
                    html.A("Primary", className='text-default fw-bold me-3', href='#'),
                    html.A([
                        Svg([
                            Path(clipRule='evenodd', d='M2 9.5A3.5 3.5 0 005.5 13H9v2.586l-1.293-1.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L11 15.586V13h2.5a4.5 4.5 0 10-.616-8.958 4.002 4.002 0 10-7.753 1.977A3.5 3.5 0 002 9.5zm9 3.5H9V8a1 1 0 012 0v5z', fillRule='evenodd')
                        ], className='icon icon-xxs me-2', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg'),
                        "Icon Left"
                    ], className='text-primary d-inline-flex align-items-center me-3', href='#'),
                    html.A([
                        "Icon Right",
                        Svg([
                            Path(clipRule='evenodd', d='M2 9.5A3.5 3.5 0 005.5 13H9v2.586l-1.293-1.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L11 15.586V13h2.5a4.5 4.5 0 10-.616-8.958 4.002 4.002 0 10-7.753 1.977A3.5 3.5 0 002 9.5zm9 3.5H9V8a1 1 0 012 0v5z', fillRule='evenodd')
                        ], className='icon icon-xxs ms-2', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg')
                    ], className='text-primary d-inline-flex align-items-center', href='#'),

                    html.Div(html.H2("Tooltips", className='h5'), className='mb-3 mt-5'),
                    html.Button("Tooltip on top", className='btn btn-secondary', title='', type='button', **{"data-bs-original-title": "Tooltip on top", "data-bs-placement": "top", "data-bs-toggle": "tooltip"}),
                    html.Button("Tooltip on right", className='btn btn-secondary', title='', type='button', **{"data-bs-original-title": "Tooltip on right", "data-bs-placement": "right", "data-bs-toggle": "tooltip"}),
                    html.Button("Tooltip on bottom", className='btn btn-secondary', title='', type='button', **{"data-bs-original-title": "Tooltip on bottom", "data-bs-placement": "bottom", "data-bs-toggle": "tooltip"}),
                    html.Button("Tooltip on left", className='btn btn-secondary', title='', type='button', **{"data-bs-original-title": "Tooltip on left", "data-bs-placement": "left", "data-bs-toggle": "tooltip"}),

                    html.Div(html.H2("Popovers", className='h5'), className='mb-3 mt-5'),
                    html.Button("Popover on top", className='btn btn-secondary', title='', type='button', **{"data-bs-container": "body", "data-bs-content": "Top popover", "data-bs-original-title": "", "data-bs-placement": "top", "data-bs-toggle": "popover"}),
                    html.Button("Popover on right", className='btn btn-secondary', title='', type='button', **{"data-bs-container": "body", "data-bs-content": "Right popover", "data-bs-original-title": "", "data-bs-placement": "right", "data-bs-toggle": "popover"}),
                    html.Button("Popover on bottom", className='btn btn-secondary', title='', type='button', **{"data-bs-container": "body", "data-bs-content": "Bottom popover", "data-bs-original-title": "", "data-bs-placement": "bottom", "data-bs-toggle": "popover"}),
                    html.Button("Popover on left", className='btn btn-secondary', title='', type='button', **{"data-bs-container": "body", "data-bs-content": "Left popover", "data-bs-original-title": "", "data-bs-placement": "left", "data-bs-toggle": "popover"}),

                    html.Div(html.H2("Choose your color", className='h5'), className='mb-3 mt-5'),
                    html.Div([
                        html.Small("Main", className='text-uppercase fw-bold')
                    ], className='mb-3 mt-5'),
                    html.Button("Primary", className='btn btn-primary', type='button'),
                    html.Button("Secondary", className='btn btn-secondary', type='button'),
                    html.Button("Tertiary", className='btn btn-tertiary', type='button'),
                    html.Button("Info", className='btn btn-info', type='button'),
                    html.Button("Success", className='btn btn-success', type='button'),
                    html.Button("Warning", className='btn btn-warning', type='button'),
                    html.Button("Danger", className='btn btn-danger', type='button'),
                    html.Button("Dark", className='btn btn-gray-800', type='button'),
                    html.Button("Gray", className='btn btn-gray-200', type='button'),
                    html.Button("Light", className='btn btn-gray-50', type='button'),
                    html.Button("White", className='btn btn-white', type='button'),

                    html.Div(html.Small("Outline", className='text-uppercase fw-bold'), className='mb-3 mt-5'),
                    html.Button("Primary", className='btn btn-outline-primary', type='button'),
                    html.Button("Secondary", className='btn btn-outline-secondary', type='button'),
                    html.Button("Tertiary", className='btn btn-outline-tertiary', type='button'),
                    html.Button("Info", className='btn btn-outline-info', type='button'),
                    html.Button("Success", className='btn btn-outline-success', type='button'),
                    html.Button("Danger", className='btn btn-outline-danger', type='button'),
                    html.Button("Dark", className='btn btn-outline-gray-800', type='button'),
                    html.Button("Gray", className='btn btn-outline-gray-500', type='button'),

                    html.Div(html.Small("Round Outline", className='text-uppercase fw-bold'), className='mb-3 mt-5'),
                    html.Button("Primary", className='btn btn-pill btn-outline-primary', type='button'),
                    html.Button("Secondary", className='btn btn-pill btn-outline-secondary', type='button'),
                    html.Button("Tertiary", className='btn btn-pill btn-outline-tertiary', type='button'),
                    html.Button("Info", className='btn btn-pill btn-outline-info', type='button'),
                    html.Button("Success", className='btn btn-pill btn-outline-success', type='button'),
                    html.Button("Danger", className='btn btn-pill btn-outline-danger', type='button'),
                    html.Button("Dark", className='btn btn-pill btn-outline-gray-800', type='button'),
                    html.Button("Gray", className='btn btn-pill btn-outline-gray-500', type='button'),

                    html.Div(html.Small("Links", className='text-uppercase fw-bold'), className='mb-3 mt-5'),
                    html.A("Default", className='text-default me-3', href='#'),
                    html.A("Primary", className='text-primary me-3', href='#'),
                    html.A("Secondary", className='text-secondary me-3', href='#'),
                    html.A("Tertiary", className='text-tertiary me-3', href='#'),
                    html.A("Info", className='text-info me-3', href='#'),
                    html.A("Success", className='text-success me-3', href='#'),
                    html.A("Danger", className='text-danger me-3', href='#'),
                    html.A("Dark", className='text-dark me-3', href='#'),
                    html.A("Gray", className='text-gray', href='#'),

                    html.Div([
                        html.Div([
                            html.Div(html.H2("Social Buttons", className='h5 fw-bold'), className='mb-4 mt-5'),
                            FACEBOOK_TEXT_BTN, html.Br(),
                            TWITTER_TEXT_BTN, html.Br(),
                            YOUTUBE_TEXT_BTN, html.Br(),
                            GITHUB_TEXT_BTN, html.Br(),
                            PAYPAL_TEXT_BTN, html.Br(),
                            FOLLOW_US_TEXT_BTN
                        ], className='col-lg-4 col-md-6'),

                        html.Div([
                            html.Div(html.H2("Only Icon", className='h5'), className='mb-4 mt-5'),
                            FACEBOOK_BTN, html.Br(),
                            TWITTER_BTN, html.Br(),
                            YOUTUBE_BTN, html.Br(),
                            GITHUB_BTN, html.Br(),
                            PAYPAL_BTN, html.Br(),
                            FOLLOW_US_BTN
                            ], className='col-12 col-lg-6')
                    ], className='row')
                ], className='card-body')
            ], className='card border-light shadow-sm components-section')
        ], className='col-12 mb-4')
    ])


layout = html.Div([
        mobileNavBar(),
        sideBar(),
        html.Main([
            topNavBar(),
            html.Div([
                breadCrumbs(),
                banner()
            ], className='py-4'),
            buttons(),
            footer()
        ], className='content')
    ])