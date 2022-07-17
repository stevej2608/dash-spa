from dash import html
from ..icons.hero import HOME

def breadCrumbs(trail: list):

    # TODO: Make this interactive

    def links():
        result = []
        trail.insert(0, HOME)
        for el in trail:
            if el != trail[-1]:
                link = html.Li(html.A(el, href='#'), className='breadcrumb-item')
            else:
                link = html.Li(el, className='breadcrumb-item active', **{"aria-current": "page"})
            result.append(link)
        return result

    return  html.Nav([
        html.Ol(links(), className='breadcrumb breadcrumb-dark breadcrumb-transparent')
    ], className='d-none d-md-inline-block', **{"aria-label": "breadcrumb"})