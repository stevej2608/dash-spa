from dash import html,dcc

from ..icons.hero import ICON

def _categoryRank(category, categoryIcon, rank, rankIcon):
    return html.Div([
        html.Div([
            html.Div([
                categoryIcon,
                category
            ], className='h6 mb-0 d-flex align-items-center')
        ]),
        html.Div([
            dcc.Link([
                rank,
                rankIcon
            ], href='#', className='d-flex align-items-center fw-bold')
        ])
    ], className='d-flex align-items-center justify-content-between border-bottom pb-3')

def _categoryRankExt(category, categoryIcon, rank, notes, upDownIcon, rankIcon):
    return html.Div([
        html.Div([
            html.Div([
                categoryIcon,
                category
            ], className='h6 mb-0 d-flex align-items-center'),
            html.Div([
                notes,
                upDownIcon
            ], className='small card-stats')
        ]),
        html.Div([
            dcc.Link([
                rank,
                rankIcon
            ], href='#', className='d-flex align-items-center fw-bold'),
        ])
    ], className='d-flex align-items-center justify-content-between border-bottom pb-3')


def rankingPanel():
    return html.Div([
        html.Div([
            html.Div([
                _categoryRank("Global Rank", ICON.EARTH, '#755', ICON.ICON1),
                _categoryRankExt("Country Rank", ICON.COUNTRY, '#32', "United States", ICON.UP_ARROW.XS, ICON.ICON1),
                _categoryRankExt("Category Rank", ICON.CATEGORY, '#11', "Computers Electronics > Technology", ICON.UP_ARROW.XS, ICON.ICON1),
           ], className='card-body')
        ], className='card border-0 shadow')
    ], className='col-12 px-0 mb-4')
