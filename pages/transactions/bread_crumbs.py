
from dash import html
from dash_svg import Svg, Path

def breadCrumbs():
    return  html.Nav([
        html.Ol([
            html.Li([
                html.A([
                    Svg([
                        Path(strokeLinecap='round', strokeLinejoin='round', strokeWidth='2', d='M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6')
                    ], className='icon icon-xxs', fill='none', stroke='currentColor', viewBox='0 0 24 24', xmlns='http://www.w3.org/2000/svg')
                ], href='#')
            ], className='breadcrumb-item'),
            html.Li([
                html.A("Volt", href='#')
            ], className='breadcrumb-item'),
            html.Li("Transactions", className='breadcrumb-item active', **{"aria-current": "page"})
        ], className='breadcrumb breadcrumb-dark breadcrumb-transparent')
    ], className='d-none d-md-inline-block', **{"aria-label": "breadcrumb"})

