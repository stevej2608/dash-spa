from dash import html, dcc

from ..icons.hero import SEARCH

def searchForm():
    return  html.Form([
        html.Div([
            html.Span([
                SEARCH
            ], className='input-group-text', id='topbar-addon'),
            dcc.Input(type='text', className='form-control', id='topbarInputIconLeft', placeholder='Search')
        ], className='input-group input-group-merge search-bar')
    ], className='navbar-search form-inline', id='navbar-search-main')


def topNavBar():
    """"Top navbar, search form ..."""
    return html.Nav([
        html.Div([
            html.Div([
                html.Div([
                    searchForm()
                ], className='d-flex align-items-center')
            ], className='d-flex justify-content-between w-100', id='navbarSupportedContent')
        ], className='container-fluid px-0')
    ], className='navbar navbar-top navbar-expand navbar-dashboard navbar-dark ps-0 pe-2 pb-0')
