from dash import html
from .navbar import NavbarBase

class Footer(NavbarBase):

    style = '''
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f5f5f5;
            }
        '''

    def __init__(self, title=None):
        super().__init__()
        self.title=title

    def layout(self):
        text = self.title
        if text:
            return html.Footer([
                html.Div([
                    html.P(text, id='footer', className='text-center font-italic', style={'marginTop': 10})
                ], className='containers')
            ], className='footer')
        else:
            return None
