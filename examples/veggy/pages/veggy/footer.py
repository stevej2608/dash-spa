from dash import html

WS = "\n"

def footer():
    return html.Footer([
        html.P([
            html.A("View Source on Github", href='https://github.com/sivadass/react-shopping-cart', target='_blank'),
            html.Span("/"),
            html.A("Need any help?", href='mailto:contact@sivadass.in', target='_blank'),
            html.Span("/"),
            html.A("Say Hi on Twitter", href='https://twitter.com/NSivadass', target='_blank'),
            html.Span("/"),
            html.A("Read My Blog", href='https://sivadass.in', target='_blank')
        ], className='footer-links'),
        html.P(["© 2017", WS, html.Strong("Veggy"), WS, "- Organic Green Store" ])
    ])