from dash import html, dcc

from ..icons.hero import CLIPBOARD

def _progressBar100(value, color='success', margin='mb-0'):
    return html.Div([
        html.Div(role='progressbar', className=f'progress-bar bg-{color}', style={"width": f"{value}%"}, **{"aria-valuenow": f"{value}", "aria-valuemin": "0", "aria-valuemax": "100"}),
    ], className=f'{margin} progress')


def _progressDetails(title, value, color="success"):
    return html.Div([
        html.Div([
            CLIPBOARD
        ], className='col-auto'),
        html.Div([
            html.Div([
                html.Div([
                    html.Div(title, className='h6 mb-0'),
                    html.Div([
                        html.Span(f"{value} %")
                    ], className='small fw-bold text-gray-500')
                ], className='progress-info'),
                _progressBar100(value,color=color, margin='mb-0')
            ], className='progress-wrapper')
        ], className='col')
    ], className='row mb-4')


def progressTrack():
    return html.Div([
        html.Div([
            html.Div([
                html.H2("Progress track", className='fs-5 fw-bold mb-0'),
                dcc.Link("See tasks", href='#', className='btn btn-sm btn-primary')
            ], className='card-header border-bottom d-flex align-items-center justify-content-between'),
            html.Div([
                _progressDetails("Rocket - SaaS Template", 75),
                _progressDetails("Themesberg - Design System", 60),
                _progressDetails("Homepage Design in Figma", 45, color='warning'),
                _progressDetails("Backend for Themesberg v2", 34, color='danger'),
            ], className='card-body')
        ], className='card border-0 shadow')
    ], className='col-12 col-xxl-6 mb-4')

