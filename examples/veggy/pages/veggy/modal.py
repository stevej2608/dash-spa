from dash import html, dcc

def modal():
    return html.Div([
            html.Div([
                html.Button("×", type='button', className='close'),
                html.Div([
                    html.Div([
                        html.Img()
                    ], className='quick-view-image'),
                    html.Div([
                        html.Span(className='product-name'),
                        html.Span(className='product-price')
                    ], className='quick-view-details')
                ], className='quick-view')
            ], className='modal')
        ], className='modal-wrapper')
