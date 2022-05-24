from dash import html
from .navbar import NavbarBase


class Footer(NavbarBase):

    xstyle = '''
        .spa_footer {
            background-color: #c6c4c4;
            }
        '''

    def __init__(self, title=None):
        super().__init__()
        self.title=title

    def layout(self):
        text = self.title
        if text:
            return html.Div([
                    html.P(text, id='footer', className='text-center font-italic', style={'marginTop': 10})
                ], className='spa_footer')
        else:
            return None
