from collections import OrderedDict
import pandas as pd
from dash import html
from .basic_table import BasicTable

data = OrderedDict([

    ('Country',['United States', 'Canada', 'United Kingdom', 'France', 'Japan', 'Germany']),
    ('All',['106', '76', '147', '112', '115', '220']),
    ('All Change',['-5', '17', '10', '3', '-12', '-56']),
    ('Travel & Local',['3', '4', '5', '5', '6', '7']),
    ('Travel & Local Change',['=', '=', '=', '1', '-1', '-3']),
    ('Widgets',['32', '30', '34', '34', '37', '30']),
    ('Widgets Change',['3', '3', '7', '-2', '-5', '2']),
    ])

FLAGS = {
    "United States": '../../assets/img/flags/united-states-of-america.svg',
    "Canada": '../../assets/img/flags/canada.svg',
    "United Kingdom": '../../assets/img/flags/united-kingdom.svg',
    "France": '../../assets/img/flags/france.svg',
    "Japan": '../../assets/img/flags/japan.svg',
    "Germany": '../../assets/img/flags/germany.svg',
}


df = pd.DataFrame.from_dict(data)

class TravelTable(BasicTable):

    def tableRow(self, index, args):

        country, all, change, tal, talCh, widgets, widgetsCh = args.values()

        return  html.Tr([
            html.Td([
                html.A([
                    html.Img(className='me-2 image image-small rounded-circle', alt='Image placeholder', src=FLAGS[country]),
                    html.Div([
                        html.Span(country, className='h6')
                    ])
                ], href='#', className='d-flex align-items-center')
            ], className='border-0'),
            html.Td(all, className='border-0 fw-bold'),
            self.numberAndArrow(change),
            html.Td(tal, className='border-0 fw-bold'),
            self.numberAndArrow(talCh),
            html.Td(widgets, className='border-0'),
            self.numberAndArrow(widgetsCh),

        ])

table = TravelTable(
    data=df.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in df.columns])

def table2():
    return html.Div([
        html.Div([
            html.Div(table, className='table-responsive')
        ], className='card-body')
    ], className='card border-0 shadow')
