from dash import html

def buttonBar(lhs=[], rhs=[]):
    lhs = lhs if isinstance(lhs, list) else [lhs]
    rhs = rhs if isinstance(rhs, list) else [rhs]
    return html.Div([
        *lhs,
        html.Div(rhs, className='d-flex flex-md-nowrap align-items-center')
    ], className='d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center py-4')
