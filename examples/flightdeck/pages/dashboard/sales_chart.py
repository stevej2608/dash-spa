from dash import html, dcc
from dash_chartist import DashChartist

data = {
    "labels": ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    "series": [ [0, 10, 30, 40, 80, 60, 100] ]
}

options = {
    'low': 0,
    'showArea': True,
    'fullWidth': True,
    'axisX': {
        # On the x-axis start means top and end means bottom
        'position': 'end',
        'showGrid': True
        },
    'axisY': {
        # On the y-axis start means left and end means right
        'showGrid': False,
        'showLabel': False,
        }
    }

chartType = 'Line'

def _chartHeader():
    return  html.Div([
        html.Div([
            html.Div("Sales Value", className='fs-5 fw-normal mb-2'),
            html.H2("$10,567", className='fs-3 fw-extrabold'),
            html.Div([
                html.Span("Yesterday", className='fw-normal me-2'),
                html.Span(className='fas fa-angle-up text-success'),
                html.Span("10.57%", className='text-success fw-bold')
            ], className='small mt-2')
        ], className='d-block mb-3 mb-sm-0'),
        html.Div([
            dcc.Link("Month", href='#', className='btn btn-secondary text-dark btn-sm me-2'),
            dcc.Link("Week", href='#', className='btn btn-sm me-3')
        ], className='d-flex ms-auto')
    ], className='card-header d-sm-flex flex-row align-items-center flex-0')


def salesChart():
    return  html.Div([
        html.Div([
            _chartHeader(),
            html.Div([
                DashChartist(className='ct-chart-sales-value ct-double-octave ct-series-g', type=chartType, options=options, tooltips=True, data=data)
            ], className='card-body p-2')
        ], className='card bg-yellow-100 border-0 shadow')
    ], className='col-12 mb-4')
